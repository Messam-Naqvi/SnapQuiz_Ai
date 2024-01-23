import React from "react";
import "./Home.css";
import quizImage from "./animiated_photo_of_students_thinking_about_conte.jpg"; // Replace with actual path
import { Link } from 'react-router-dom';
const Home = () => {
  return (
    <>
      <br />
      <br />
      <div className="container1 text-center">
        <h1 className="display-2 text-white fw-bold">Welcome to Snap Quiz</h1>
      </div>
      <br />
      <br />
      <br />
      <div className="container">
        <div className="row align-items-center">
          <div className="col-lg-6 mb-4">
            <img
              style={{
                width: "60%", // Adjusted to use 100% width
                borderRadius: "20px",
              }}
              src={quizImage}
              alt="Quiz Image"
            />
          </div>
          <div className="col-lg-6" style={{ fontFamily: 'times new roman' }}> {/* this text div */}
            <div className="text-white">
              <h2 style={{ fontSize: '41px', marginBottom: '20px' }}>Why Choose Snap Quiz?</h2>
              <p style={{ fontSize: '19px', lineHeight: '1.6' }}>
                Say goodbye to passive learning! With Snap Quiz, you'll actively engage with the material through our interactive quizzes. Test your knowledge, reinforce key concepts, and track your progress effortlessly.
              </p>
              <p style={{ fontSize: '19px', lineHeight: '1.6' }}>
                Experience a new way of learning that's both effective and enjoyable.
              </p>
              <button className="btn btn-3d btn-success mt-4">
        <Link to="/quiz" style={{ textDecoration: 'none', color: 'inherit' }}>
          Get Started
        </Link>
      </button>

            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Home;
