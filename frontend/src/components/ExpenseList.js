import React, { useState, useEffect } from "react";
import axios from "axios";
import ExpenseItem from "./ExpenseItem";
import ExpenseForm from "./ExpenseForm";
import { toast } from "react-toastify";

const BASE = "http://localhost:8000/expenses";

const ExpenseList = () => {
  const [expenses, setExpenses] = useState([]);
  const [editExpense, setEditExpense] = useState(null);
  const [total, setTotal] = useState(0);
  const [categorySummary, setCategorySummary] = useState({});

  const fetchExpenses = async () => {
    try {
      const res = await axios.get(BASE);
      const data = Array.isArray(res.data) ? res.data : [];
      setExpenses(data);

      const totalAmount = data.reduce((s, e) => s + (Number(e.amount) || 0), 0);
      setTotal(totalAmount);

      const summary = {};
      data.forEach((e) => {
        const cat = e.category || "Uncategorized";
        summary[cat] = (summary[cat] || 0) + (Number(e.amount) || 0);
      });
      setCategorySummary(summary);
    } catch (err) {
      console.error("Fetch error:", err);
      toast.error("Failed to load expenses (check backend).");
    }
  };

  useEffect(() => {
    fetchExpenses();
  }, []);

  return (
    <div className="panel">
      <div className="top-row">
        <div className="summary-card">
          <div className="summary-label">Total Expenses</div>
          <div className="summary-value">₹{total.toLocaleString()}</div>
        </div>

        <div className="summary-card small">
          <div className="summary-label">Categories</div>
          <div className="category-list">
            {Object.keys(categorySummary).length === 0 ? (
              <div className="muted">No categories yet</div>
            ) : (
              Object.entries(categorySummary).map(([cat, amt]) => (
                <div key={cat} className="cat-row">
                  <span>{cat}</span>
                  <span>₹{Number(amt).toLocaleString()}</span>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      <ExpenseForm
        expenseToEdit={editExpense}
        onSuccess={() => {
          setEditExpense(null);
          fetchExpenses();
        }}
      />

      <div className="list">
        {expenses.length === 0 ? (
          <p className="muted">No expenses found. Add one above.</p>
        ) : (
          expenses.map((exp) => (
            <ExpenseItem
              key={exp._id || exp.id}
              expense={exp}
              onEdit={(e) => setEditExpense(e)}
              onDelete={fetchExpenses}
            />
          ))
        )}
      </div>
    </div>
  );
};

export default ExpenseList;
