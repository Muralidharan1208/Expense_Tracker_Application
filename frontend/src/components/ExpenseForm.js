import React, { useState, useEffect } from "react";
import axios from "axios";
import { toast } from "react-toastify";

const BASE = "http://localhost:8000/expenses";

const ExpenseForm = ({ expenseToEdit, onSuccess }) => {
  const [title, setTitle] = useState("");
  const [amount, setAmount] = useState("");
  const [category, setCategory] = useState("");
  const [date, setDate] = useState("");

  useEffect(() => {
    if (expenseToEdit) {
      setTitle(expenseToEdit.title || "");
      setAmount(expenseToEdit.amount || "");
      setCategory(expenseToEdit.category || "");
      // keep only the date part if ISO string present
      setDate(expenseToEdit.date ? expenseToEdit.date.split("T")[0] : "");
    } else {
      setTitle("");
      setAmount("");
      setCategory("");
      setDate("");
    }
  }, [expenseToEdit]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title || !amount || !category || !date) {
      toast.error("Please fill all fields.");
      return;
    }

    const payload = { title, amount: Number(amount), category, date };
    try {
      if (expenseToEdit && (expenseToEdit._id || expenseToEdit.id)) {
        const id = expenseToEdit._id || expenseToEdit.id;
        await axios.put(`${BASE}/${id}`, payload);
        toast.success("Expense updated!");
      } else {
        await axios.post(BASE, payload);
        toast.success("Expense added!");
      }
      onSuccess();
      // clear local form (in case API returns stale)
      setTitle("");
      setAmount("");
      setCategory("");
      setDate("");
    } catch (err) {
      console.error("Save error:", err);
      toast.error("Failed to save expense (check backend).");
    }
  };

  return (
    <form className="expense-form" onSubmit={handleSubmit}>
      <input
        className="input"
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
      />
      <input
        className="input"
        placeholder="Amount"
        type="number"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        required
      />
      <input
        className="input"
        placeholder="Category"
        value={category}
        onChange={(e) => setCategory(e.target.value)}
        required
      />
      <input
        className="input"
        type="date"
        value={date}
        onChange={(e) => setDate(e.target.value)}
        required
      />
      <button className="btn" type="submit">
        {expenseToEdit ? "Update Expense" : "Add Expense"}
      </button>
    </form>
  );
};

export default ExpenseForm;
