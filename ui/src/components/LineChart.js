import { Line, Chart } from 'react-chartjs-2';
import { Chart as ChartJS, registerables } from 'chart.js';

ChartJS.register(...registerables);

export default function LineChart({chartTitle, datasets, yAxis}) {
    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: chartTitle,
            },
        },
        scales: {
            y: yAxis ? {reverse: true, ...yAxis } : {}
        }
    };

    const labels = [];
    for (let i = 0; i < 38; i++) {
        labels.push(i + 1);
    }


    const data = {
        labels,
        datasets: datasets
    };

    return (
        <Line options={options} data={data} />
    );
}
