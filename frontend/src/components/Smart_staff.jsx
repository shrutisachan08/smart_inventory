import React, { useState } from "react";
import axios from "axios";
import { MapPin, LocateFixed, Send, AlertCircle, BadgeCheck } from "lucide-react";

const AssignTaskPage = () => {
  const [latitude, setLatitude] = useState("");
  const [longitude, setLongitude] = useState("");
  const [description, setDescription] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleAssign = async () => {
    setResult(null);
    setError(null);
    try {
      const formData = new URLSearchParams();
      formData.append("latitude", latitude);
      formData.append("longitude", longitude);
      formData.append("description", description);

      const response = await axios.post("http://127.0.0.1:5002/", formData);
      const htmlString = response.data;
      const parser = new DOMParser();
      const doc = parser.parseFromString(htmlString, "text/html");
      const assignedTo = doc.querySelector("h3");
      const distance = doc.querySelector("p:nth-of-type(1)");
      const task = doc.querySelector("p:nth-of-type(2)");

      if (assignedTo && distance && task) {
        setResult({
          StaffID: assignedTo.textContent,
          Distance: distance.textContent,
          Task: task.textContent,
        });
      } else {
        setError("Assignment failed or no available staff.");
      }
    } catch (err) {
      setError("Server error or invalid input.");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-950 via-purple-900 to-black text-white px-4 py-16">
      <div className="max-w-2xl mx-auto bg-white/10 p-10 rounded-2xl shadow-xl border border-purple-500">
        <h1 className="text-4xl font-bold text-purple-300 mb-8 flex items-center gap-3">
          <MapPin size={32} /> Smart Staff Task Assignment
        </h1>

        <div className="grid gap-6">
          <div>
            <label className="block mb-1 text-sm text-white/80">Latitude</label>
            <input
              type="text"
              placeholder="Enter Latitude"
              value={latitude}
              onChange={(e) => setLatitude(e.target.value)}
              className="w-full px-4 py-2 rounded-lg bg-black/20 border border-purple-400 text-white placeholder:text-white/50"
            />
          </div>

          <div>
            <label className="block mb-1 text-sm text-white/80">Longitude</label>
            <input
              type="text"
              placeholder="Enter Longitude"
              value={longitude}
              onChange={(e) => setLongitude(e.target.value)}
              className="w-full px-4 py-2 rounded-lg bg-black/20 border border-purple-400 text-white placeholder:text-white/50"
            />
          </div>

          <div>
            <label className="block mb-1 text-sm text-white/80">Task Description</label>
            <input
              type="text"
              placeholder="Enter Task Description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full px-4 py-2 rounded-lg bg-black/20 border border-purple-400 text-white placeholder:text-white/50"
            />
          </div>

          <button
            onClick={handleAssign}
            className="mt-4 bg-purple-700 hover:bg-purple-800 transition px-6 py-2 rounded-lg flex items-center gap-2 justify-center text-white font-semibold shadow-md"
          >
            <Send size={18} /> Assign Task
          </button>
        </div>

        {result && (
          <div className="mt-8 bg-emerald-800/20 border border-emerald-400 p-5 rounded-xl shadow-inner">
            <h2 className="text-xl font-semibold text-emerald-300 flex items-center gap-2 mb-3">
              <BadgeCheck /> Assignment Successful
            </h2>
            <p className="text-white/90">{result.StaffID}</p>
            <p className="text-white/90">{result.Distance}</p>
            <p className="text-white/90">{result.Task}</p>
          </div>
        )}

        {error && (
          <div className="mt-6 bg-red-800/20 border border-red-500 p-4 rounded-lg text-red-300 flex items-center gap-3">
            <AlertCircle /> {error}
          </div>
        )}
      </div>
    </div>
  );
};

export default AssignTaskPage;
