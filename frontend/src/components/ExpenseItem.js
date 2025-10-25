import React from "react";
import axios from "axios";
import { toast } from "react-toastify";

const BASE = "http://localhost:8000/expenses";

const ExpenseItem = ({ expense, onEdit, onDelete }) => {
  const id = expense._id || expense.id;

  const handleDelete = async () => {
    if (!window.confirm("Delete this expense?")) return;
    try {
      await axios.delete(`${BASE}/${id}`);
      toast.success("Deleted");
      onDelete();
    } catch (err) {
      console.error("Delete error:", err);
      toast.error("Failed to delete");
    }
  };

  return (
    <div className="expense-card">
      <div className="expense-top">
        <div className="expense-title">{expense.title}</div>
        <div className="expense-amt">₹{Number(expense.amount).toLocaleString()}</div>
      </div>
      <div className="expense-meta">
        <div>Category: <strong>{expense.category || "—"}</strong></div>
        <div>Date: <strong>{(expense.date || "").split("T")[0]}</strong></div>
      </div>

      <div className="expense-actions">
        <button className="btn small" onClick={() => onEdit(expense)}>Edit</button>
        <button className="btn small red" onClick={handleDelete}>Delete</button>
      </div>
    </div>
  );
};

export default ExpenseItem;
