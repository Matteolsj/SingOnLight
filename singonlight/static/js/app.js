async function clear_game_data() {
    const response = await fetch('/api/data/reset', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
    });
    if (response.ok) {
        await refresh_game_data();
    }
}

async function refresh_game_data() {
    const response = await fetch('/api/data/scores');
    if (response.ok) {
        showChart(await response.json());
    }
}

function showChart(chartData) {
    Highcharts.chart('container', {
        chart: { type: 'column' },
        title: { text: 'Scores Across Games' },
        subtitle: {
            text: chartData.every(([, count]) => count === 0)
                ? 'No games recorded yet.'
                : ''
        },
        xAxis: {
            type: 'category',
            labels: {
                autoRotation: [-45, -90],
                style: { fontSize: '13px', fontFamily: 'Verdana, sans-serif' }
            }
        },
        yAxis: { min: 0, title: { text: 'Games Played' } },
        legend: { enabled: false },
        tooltip: { pointFormat: 'Games played: <b>{point.y:.0f}</b>' },
        series: [{
            name: 'Scores',
            colors: [
                '#9b20d9', '#861ec9', '#7010f9', '#6225ed', '#533be1',
                '#4551d5', '#3667c9', '#277dbd', '#1693b1', '#03c69b', '#00f194'
            ],
            colorByPoint: true,
            groupPadding: 0,
            data: chartData,
            dataLabels: {
                enabled: true,
                rotation: -90,
                color: '#FFFFFF',
                inside: true,
                verticalAlign: 'top',
                format: '{point.y:.0f}',
                y: 10,
                style: { fontSize: '13px', fontFamily: 'Verdana, sans-serif' }
            }
        }]
    });
}

async function show_story_animation() {
    const dragonGif = document.getElementById('gifDragon');
    const gifSource = dragonGif.src;
    dragonGif.src = '';
    dragonGif.src = gifSource;
    dragonGif.classList.remove('hidden');
    dragonGif.classList.add('visible');

    setTimeout(async () => {
        dragonGif.classList.remove('visible');
        dragonGif.classList.add('hidden');

        const response = await fetch('/api/play/story', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
        });
        const result = await response.json();

        if (result.state === 'won') {
            document.getElementById('level').innerText = result.level;
            document.getElementById('storyButton').click();
        } else if (result.state === 'lost') {
            const gameOverImage = document.getElementById('gameOver');
            gameOverImage.classList.remove('hidden');
            gameOverImage.classList.add('visible');
        } else if (result.state === 'finished') {
            const victoryImage = document.getElementById('victory');
            victoryImage.classList.remove('hidden');
            victoryImage.classList.add('visible');
        }
    }, 2650);
}
