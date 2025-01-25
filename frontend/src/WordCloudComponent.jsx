import React, { memo } from 'react';
import ReactWordcloud from 'react-wordcloud';

const WordCloudComponent = memo(({ words }) => {
  if (!words || words.length === 0) return <div>No data available for the word cloud.</div>;

  const options = {
    rotations: 2,
    rotationAngles: [-90, 0],
    fontSizes: [15, 60],
  };

  return <ReactWordcloud words={words} options={options} />;
});

export default WordCloudComponent;
