import React, { useState } from "react";
import axios from "axios";
import "./Quiz.css";
import { FaFileAlt, FaGlobe, FaRegSmile, FaMeh, FaAngry } from "react-icons/fa";

const Quiz = () => {
  const [quizType, setQuizType] = useState("content");
  const [content, setContent] = useState("");
  const [websiteUrl, setWebsiteUrl] = useState("");
  const [difficulty, setDifficulty] = useState("easy");
  const [selectedChoice, setSelectedChoice] = useState(null);
  const [fetchedData, setFetchedData] = useState([]);
  const [error, setError] = useState("");
  const [wordCount, setWordCount] = useState(0);

  const isValidUrl = (url) => {
    try {
      new URL(url);
      return true;
    } catch (error) {
      return false;
    }
  };

  const handleContentClick = () => {
    setSelectedChoice(
      `You have chosen Content Quiz of Difficulty ${
        difficulty.charAt(0).toUpperCase() + difficulty.slice(1)
      }`
    );
  };

  const handleWebsiteClick = () => {
    setSelectedChoice(
      `You have chosen Website Quiz of Difficulty ${
        difficulty.charAt(0).toUpperCase() + difficulty.slice(1)
      }`
    );
  };

  const handleDifficultyClick = (diff) => {
    setSelectedChoice(
      `You have chosen  ${
        quizType === "content" ? "Content Quiz" : "Website Quiz"
      } of Difficulty '${diff.charAt(0).toUpperCase() + diff.slice(1)}'.`
    );
    setDifficulty(diff);
  };

  const handleContentChange = (e) => {
    const newContent = e.target.value;
    setContent(newContent);

    const words = newContent.trim().split(/\s+/);
    setWordCount(words.length);

    if (words.length < 140 || words.length > 195) {
      setError("Word count must be between 140 and 195.");
    } else {
      setError("");
    }
  };

  const handleCreateQuiz = async () => {
    try {
      if (quizType === "website") {
        if (["easy", "medium", "hard"].includes(difficulty)) {
          if (!isValidUrl(websiteUrl)) {
            setError("Invalid website URL.");
            return;
          }

          const smmryResponse = await axios.get(
            `https://api.smmry.com?SM_API_KEY=508DF23869&SM_URL=${websiteUrl}`
          );

          const summarizedContent = smmryResponse.data.sm_api_content;

          const apiUrl =
            difficulty === "easy"
              ? "http://localhost:5000/api/create_quiz"
              : difficulty === "medium"
              ? "http://localhost:5000/api/generate_medium_questions"
              : "http://localhost:5000/api/hard";

          const response = await axios.post(apiUrl, {
            quizContent: summarizedContent,
          });

          // Format and structure the quiz data for display
          const formattedQuiz = response.data.processedQuiz
            ? response.data.processedQuiz.map((question) => ({
                questionNumber: question.question_number,
                questionText: question.question,
                options: question.options,
                answer: question.answer,
              }))
            : response.data.questions.map((question, index) => ({
                questionNumber: index + 1,
                questionText: question,
                options: [],  
                answer: "",  
              }));

          // Update the state with the formatted quiz data
          setFetchedData(formattedQuiz);
          setError("");
        } else {
         
          setError("Quiz creation is only supported for 'Easy,' 'Medium,' or 'Hard' difficulty.");
        }
      } else {
        if (quizType === "content" && ["easy", "medium", "hard"].includes(difficulty)) {
          const apiUrl =
            difficulty === "easy"
              ? "http://localhost:5000/api/create_quiz"
              : difficulty === "medium"
              ? "http://localhost:5000/api/generate_medium_questions"
              : "http://localhost:5000/api/hard";

          const response = await axios.post(apiUrl, {
            quizContent: content,
          });

         
          const formattedQuiz = response.data.processedQuiz
            ? response.data.processedQuiz.map((question) => ({
                questionNumber: question.question_number,
                questionText: question.question,
                options: question.options,
                answer: question.answer,
              }))
            : response.data.questions.map((question, index) => ({
                questionNumber: index + 1,
                questionText: question,
                options: [],  
                answer: "",  
              }));

         
          setFetchedData(formattedQuiz);
          setError("");
        } else {
         
          setError("Quiz creation is only supported for 'Easy,' 'Medium,' or 'Hard' difficulty.");
        }
      }
    } catch (err) {
      console.error("Error creating or fetching quiz:", err);
      setError("Error creating or fetching quiz");
    }
  };

  return (
    <>
      <br />
      <br />
      <br />
      <div className="quiz-container">
        <h1>Create a Quiz</h1>
        <div className="quiz-type">
          <h2 className="quiz-type-heading">Quiz Type:</h2>
          <div className="btn-group">
            <button
              className={`btn ${
                quizType === "content"
                  ? "btn-primary active"
                  : "btn-outline-primary"
              }`}
              onClick={() => setQuizType("content")}
            >
              <FaFileAlt className="icon" />
              Content Quiz
            </button>

            <button
              className={`btn ${
                quizType === "website"
                  ? "btn-primary active"
                  : "btn-outline-primary"
              }`}
              onClick={() => setQuizType("website")}
            >
              <FaGlobe className="icon" />
              Website Quiz
            </button>
          </div>
        </div>
        {quizType === "content" ? (
          <div>
            <label htmlFor="content">Quiz Content:</label>
            <textarea
              id="content"
              className="form-control"
              placeholder="Enter quiz content here"
              value={content}
              onChange={handleContentChange}
              rows={5}
            />
            <p>Word(s) Count: {wordCount}</p>
            <p style={{color:"red"}}>Word count must be between 140 and 195.</p>
          </div>
        ) : (
          <div>
            <label htmlFor="website-url">Website URL:</label>
            <input
              id="website-url"
              type="text"
              className="form-control"
              placeholder="Enter website URL here"
              value={websiteUrl}
              onChange={(e) => setWebsiteUrl(e.target.value)}
            />
            <p style={{color:"red"}}>URL Supported only for article websites</p>
            {error && <p style={{ color: "red" }}>{error}</p>}
          </div>
        )}
        <br />
        <div className="quiz-difficulty">
          <h2 className="quiz-difficulty-heading">Difficulty:</h2>
          <div className="btn-group">
            <button
              className={`btn ${
                difficulty === "easy"
                  ? "btn-success active"
                  : "btn-outline-success"
              }`}
              onClick={() => handleDifficultyClick("easy")}
            >
              <FaRegSmile className="icon" />
              Medium
            </button>
            <button
              className={`btn ${
                difficulty === "medium"
                  ? "btn-warning active"
                  : "btn-outline-warning"
              }`}
              onClick={() => handleDifficultyClick("medium")}
            >
              <FaMeh className="icon" />
              Easy
            </button>
            <button
              className={`btn ${
                difficulty === "hard"
                  ? "btn-danger active"
                  : "btn-outline-danger"
              }`}
              onClick={() => handleDifficultyClick("hard")}
            >
              <FaAngry className="icon" />
              Hard
            </button>
          </div>
        </div>
        {selectedChoice && <p className="quiz-choices">{selectedChoice}</p>}
        <div className="submit-btn">
          <button
            className="btn btn-lg btn-primary"
            onClick={handleCreateQuiz}
            disabled={quizType === "content" && (wordCount < 140 || wordCount > 195)}
          >
            Create Quiz
          </button>
        </div>
        <br />
        {fetchedData.length > 0 && (
          <div>
            <h2>Your Quiz:</h2>
            <ul>
              {fetchedData.map((question) => (
                <li key={question.questionNumber}>
                  <strong>Question {question.questionNumber}:</strong> {question.questionText} 
                  <br />
                  <br />
                  <ul>
                    {question.options.map((option, index) => (
                      <li key={index}>{option}</li>
                      
                    ))}
                  </ul>
                  {(quizType === "content" || quizType === "website") && (difficulty==="hard" || difficulty==="medium") ? null : (
                    <p><strong>Answer:</strong> {question.answer}</p>
                    
                  )}
                </li>
                
              ))}
            </ul>
           
          </div>
        )}
      </div>
    </>
  );
};

export default Quiz;
