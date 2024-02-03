import "./App.css";
import { BrowserRouter, Link, Route, Routes } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import Navbar from "./Components/Navbar";
import Home from "./Components/Home";
import Quiz from "./Components/Quiz";

function App() {
  return (
    <BrowserRouter>
      <div className="heiback">
        <Navbar />
        <Routes>
        <Route path="/" element={<Home />} />

          <Route path="/quiz" element={<Quiz />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
