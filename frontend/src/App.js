import React from "react";
import ExpenseList from "./components/ExpenseList";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function App() {
  return (
    <div className="App">
      <div className="container">
        <header className="app-header">
          <span className="logo">💰</span>
          <h1>Expense Tracker</h1>
        </header>

        <main>
          <ExpenseList />
        </main>

        <ToastContainer position="top-right" autoClose={2200} />
      </div>
    </div>
  );
}

export default App;
