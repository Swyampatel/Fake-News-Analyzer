import React, { useEffect, useRef } from "react";
import WordCloud from "wordcloud";

const WordCloudComponent = ({ words }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const wordArray = words.map((word) => [word.text, word.value]);
    WordCloud(canvasRef.current, {
      list: wordArray,
      gridSize: 10,
      weightFactor: 3,
      fontFamily: "Times, serif",
      color: () => (Math.random() > 0.5 ? "blue" : "red"),
      rotateRatio: 0.5,
      rotationSteps: 2,
    });
  }, [words]);

  return <canvas ref={canvasRef} width={500} height={300}></canvas>;
};

export default WordCloudComponent;
