import React, { useEffect, useRef } from 'react';
import {
  Chart as ChartJS,
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { Pie, Bar } from 'react-chartjs-2';
import './ChartsSection.css';

// Register Chart.js components
ChartJS.register(
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend
);

function ChartsSection({ deck, analysis }) {
  // Elixir Distribution Chart Data
  const elixirData = {
    labels: deck.cards.map(dc => dc.card.name),
    datasets: [
      {
        label: 'Elixir Cost',
        data: deck.cards.map(dc => dc.card.elixir_cost),
        backgroundColor: [
          'rgba(255, 99, 132, 0.7)',
          'rgba(54, 162, 235, 0.7)',
          'rgba(255, 206, 86, 0.7)',
          'rgba(75, 192, 192, 0.7)',
          'rgba(153, 102, 255, 0.7)',
          'rgba(255, 159, 64, 0.7)',
          'rgba(199, 199, 199, 0.7)',
          'rgba(83, 102, 255, 0.7)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)',
          'rgba(199, 199, 199, 1)',
          'rgba(83, 102, 255, 1)',
        ],
        borderWidth: 2,
      },
    ],
  };

  // Card Types Distribution
  const typeDistribution = {};
  deck.cards.forEach(dc => {
    const type = dc.card.card_type;
    typeDistribution[type] = (typeDistribution[type] || 0) + 1;
  });

  const typeData = {
    labels: Object.keys(typeDistribution).map(t => t.charAt(0).toUpperCase() + t.slice(1)),
    datasets: [
      {
        label: 'Card Count',
        data: Object.values(typeDistribution),
        backgroundColor: [
          'rgba(54, 162, 235, 0.7)',
          'rgba(255, 99, 132, 0.7)',
          'rgba(75, 192, 192, 0.7)',
        ],
        borderColor: [
          'rgba(54, 162, 235, 1)',
          'rgba(255, 99, 132, 1)',
          'rgba(75, 192, 192, 1)',
        ],
        borderWidth: 2,
      },
    ],
  };

  // Deck Metrics Chart
  const metricsData = {
    labels: [
      'Air Defense',
      'Splash Damage',
      'Win Conditions',
      'Spells',
      'Tanks'
    ],
    datasets: [
      {
        label: 'Count',
        data: [
          analysis.metrics.air_targeting_count,
          analysis.metrics.splash_damage_count,
          analysis.metrics.win_condition_count,
          analysis.metrics.light_spell_count + analysis.metrics.heavy_spell_count,
          analysis.metrics.tank_count
        ],
        backgroundColor: 'rgba(75, 192, 192, 0.7)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 2,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          color: '#e5e7eb',
          font: {
            size: 12
          }
        }
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: '#fff',
        bodyColor: '#fff',
        borderColor: '#4b5563',
        borderWidth: 1,
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          color: '#9ca3af',
          stepSize: 1
        },
        grid: {
          color: 'rgba(75, 85, 99, 0.2)'
        }
      },
      x: {
        ticks: {
          color: '#9ca3af'
        },
        grid: {
          color: 'rgba(75, 85, 99, 0.2)'
        }
      }
    }
  };

  const pieOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          color: '#e5e7eb',
          font: {
            size: 12
          }
        }
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: '#fff',
        bodyColor: '#fff',
        borderColor: '#4b5563',
        borderWidth: 1,
      }
    }
  };

  return (
    <div className="charts-container">
      <div className="charts-grid">
        {/* Elixir Distribution */}
        <div className="chart-card">
          <h3 className="chart-title">Elixir Distribution</h3>
          <div className="chart-wrapper">
            <Bar data={elixirData} options={chartOptions} />
          </div>
        </div>

        {/* Card Types */}
        <div className="chart-card">
          <h3 className="chart-title">Card Types</h3>
          <div className="chart-wrapper">
            <Pie data={typeData} options={pieOptions} />
          </div>
        </div>

        {/* Deck Metrics */}
        <div className="chart-card full-width">
          <h3 className="chart-title">Deck Metrics</h3>
          <div className="chart-wrapper">
            <Bar data={metricsData} options={chartOptions} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default ChartsSection;