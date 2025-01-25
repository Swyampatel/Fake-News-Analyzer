import React, { useEffect, useState } from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement } from 'chart.js';
import { Bar } from 'react-chartjs-2';
import WordCloudComponent from './WordCloudComponent';

ChartJS.register(CategoryScale, LinearScale, BarElement);

const FakeNewsDashboard = () => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/scrape')
      .then((response) => response.json())
      .then((fetchedData) => {
        if (fetchedData.fake_articles_by_month && fetchedData.true_articles_by_month) {
          setData(fetchedData);
        } else {
          setError('Data structure is incorrect or empty.');
        }
      })
      .catch((err) => setError('Error fetching data: ' + err.message));
  }, []);

  if (error) return <div>Error: {error}</div>;
  if (!data) return <div>Loading...</div>;

  const barChartData = {
    labels: data.months || [],
    datasets: [
      {
        label: 'Fake Articles',
        data: data.fake_articles_by_month || [],
        backgroundColor: 'rgba(255, 99, 132, 0.6)',
      },
      {
        label: 'True Articles',
        data: data.true_articles_by_month || [],
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
      },
    ],
  };

  const barChartOptions = {
    responsive: true,
    maintainAspectRatio: false, // Fix ResizeObserver issues
  };

  return (
    <div className="p-5">
      <h1 className="text-3xl font-bold text-center">NLP Analysis</h1>
      <div className="grid grid-cols-2 gap-4 mt-5">
        <div className="shadow-lg p-4 rounded" style={{ height: '400px' }}>
          <Bar data={barChartData} options={barChartOptions} />
          <p className="text-center mt-2 font-bold">Fake (Red) / Real (Blue) Articles by Month</p>
        </div>
        <div className="shadow-lg p-4 rounded" style={{ height: '400px' }}>
          <WordCloudComponent words={data.fake_word_cloud || []} />
          <p className="text-center mt-2 font-bold">Fake Word Cloud</p>
        </div>
      </div>
    </div>
  );
};

export default FakeNewsDashboard;
