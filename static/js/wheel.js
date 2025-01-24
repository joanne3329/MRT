class Wheel {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.stations = [];
        this.rotation = 0;
        this.isSpinning = false;
        
        // 設定畫布大小
        this.canvas.width = 500;
        this.canvas.height = 500;
        
        // 色彩對應
        this.lineColors = {
            'red': '#e3002c',
            'blue': '#0070bd',
            'brown': '#c48c31',
            'green': '#008659',
            'orange': '#f8b61c',
            'yellow': '#ffdb00'
        };
    }

    updateStations() {
        const selectedLines = Array.from(document.querySelectorAll('input[name="lines"]:checked'))
            .map(cb => cb.value);
        const excludedDistricts = Array.from(document.querySelectorAll('input[name="districts"]:checked'))
            .map(cb => cb.value);

        fetch(`/get_stations?${new URLSearchParams({
            'lines[]': selectedLines,
            'excluded_districts[]': excludedDistricts
        })}`)
        .then(response => response.json())
        .then(stations => {
            this.stations = stations;
            this.draw();
        });
    }

    draw() {
        const ctx = this.ctx;
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        const radius = Math.min(centerX, centerY) - 20;

        // 清除畫布
        ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        if (this.stations.length === 0) {
            ctx.font = '20px Arial';
            ctx.fillStyle = '#000';
            ctx.textAlign = 'center';
            ctx.fillText('請選擇至少一條捷運線', centerX, centerY);
            return;
        }

        // 繪製每個扇形
        const sliceAngle = (2 * Math.PI) / this.stations.length;
        
        this.stations.forEach((station, index) => {
            const startAngle = index * sliceAngle + this.rotation;
            const endAngle = startAngle + sliceAngle;

            // 繪製扇形
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.arc(centerX, centerY, radius, startAngle, endAngle);
            ctx.closePath();

            // 填充顏色
            ctx.fillStyle = this.getStationColor(station, index);
            ctx.fill();
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 2;
            ctx.stroke();

            // 繪製文字
            ctx.save();
            ctx.translate(centerX, centerY);
            ctx.rotate(startAngle + sliceAngle / 2);
            ctx.textAlign = 'right';
            ctx.fillStyle = '#fff';
            ctx.font = '14px Arial';
            ctx.fillText(station.name, radius - 10, 5);
            ctx.restore();
        });

        // 繪製中心圓
        ctx.beginPath();
        ctx.arc(centerX, centerY, 20, 0, 2 * Math.PI);
        ctx.fillStyle = '#fff';
        ctx.fill();
        ctx.strokeStyle = '#000';
        ctx.lineWidth = 2;
        ctx.stroke();
    }

    getStationColor(station, index) {
        // 根據站點所屬線路返回對應顏色
        const lineCode = Object.keys(this.lineColors).find(code => 
            station.line.includes(Object.values(this.lineColors).find(color => 
                color === this.lineColors[code])));
        return this.lineColors[lineCode] || '#999';
    }

    spin() {
        if (this.isSpinning) return;
        
        this.isSpinning = true;
        const spinAngle = (Math.random() * 360 + 720) * (Math.PI / 180); // 轉換為弧度
        const duration = 3000; // 3秒
        const start = performance.now();
        
        const animate = (currentTime) => {
            const elapsed = currentTime - start;
            const progress = Math.min(elapsed / duration, 1);
            
            // 使用 easeOut 效果
            const easeOut = 1 - Math.pow(1 - progress, 3);
            this.rotation = easeOut * spinAngle;
            
            this.draw();
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                this.isSpinning = false;
                this.showResult();
            }
        };
        
        requestAnimationFrame(animate);
    }

    showResult() {
        // 計算最終指向的站點
        const finalRotation = this.rotation % (2 * Math.PI);
        const sliceAngle = (2 * Math.PI) / this.stations.length;
        const selectedIndex = Math.floor(((2 * Math.PI) - (finalRotation % (2 * Math.PI))) / sliceAngle) % this.stations.length;
        const selectedStation = this.stations[selectedIndex];

        // 顯示結果
        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = `
            <h3>選中站點：${selectedStation.name}</h3>
            <p>所屬線路：${selectedStation.line}</p>
            <p>行政區：${selectedStation.district}</p>
        `;
    }
}

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('wheel');
    const wheel = new Wheel(canvas);
    
    // 監聽篩選器變化
    document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
        checkbox.addEventListener('change', () => wheel.updateStations());
    });
    
    // 監聽轉動按鈕
    document.getElementById('spin').addEventListener('click', () => wheel.spin());
    
    // 初始載入站點
    wheel.updateStations();
}); 