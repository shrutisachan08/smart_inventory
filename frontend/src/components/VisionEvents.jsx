import React, { useState, useEffect } from "react";
import axios from "axios";
import { FaRegEye, FaPlus, FaTrashAlt } from "react-icons/fa";

const VisionEvents = () => {
  const [events, setEvents] = useState([]);
  const [newEvent, setNewEvent] = useState("");

  const fetchEvents = async () => {
    try {
      const res = await axios.get("http://localhost:5000/get_vision_events");
      setEvents(res.data.events || []);
    } catch (error) {
      console.error("Failed to fetch events", error);
    }
  };

  const submitEvent = async () => {
    if (!newEvent.trim()) return;
    try {
      await axios.post("http://localhost:5000/simulate_vision_event", {
        description: newEvent,
      });
      setNewEvent("");
      fetchEvents();
    } catch (error) {
      console.error("Failed to submit event", error);
    }
  };

  const removeEvent = (indexToRemove) => {
    const updatedEvents = events.filter((_, index) => index !== indexToRemove);
    setEvents(updatedEvents);
  };

  useEffect(() => {
    fetchEvents();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-500 to-purple-800 text-white px-4 py-10 flex items-center justify-center">
      <div className="w-full max-w-5xl bg-white text-gray-800 rounded-xl shadow-lg p-10">
        <h2 className="text-4xl font-extrabold mb-6 flex items-center gap-3 text-purple-700">
          <FaRegEye /> Vision Events Monitor
        </h2>

        <div className="mb-8">
          <label className="block text-sm font-semibold mb-2 text-gray-600">
            Enter Vision Event Description:
          </label>
          <input
            type="text"
            value={newEvent}
            onChange={(e) => setNewEvent(e.target.value)}
            placeholder="E.g., Customer picked Apple from Aisle 3"
            className="w-full px-4 py-3 border border-purple-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-400"
          />
          <button
            onClick={submitEvent}
            className="mt-4 inline-flex items-center gap-2 bg-purple-600 text-white px-6 py-2.5 rounded-md hover:bg-purple-700 transition duration-200"
          >
            <FaPlus /> Simulate Event
          </button>
        </div>

        <h3 className="text-2xl font-semibold mb-4 text-purple-800">Recent Events</h3>
        <div className="space-y-4 max-h-96 overflow-y-auto pr-2">
          {events.length === 0 ? (
            <p className="text-gray-500">No events recorded yet.</p>
          ) : (
            events.map((event, index) => (
              <div
                key={index}
                className="bg-purple-100 border-l-4 border-purple-600 p-4 rounded-md shadow-sm flex justify-between items-start"
              >
                <div>
                  <p className="font-semibold text-purple-900 text-lg">
                    {event.description}
                  </p>
                  <p className="text-sm text-purple-700 mt-1">{event.timestamp}</p>
                </div>
                <button
                  onClick={() => removeEvent(index)}
                  className="text-purple-800 hover:text-red-600 transition"
                  title="Remove"
                >
                  <FaTrashAlt />
                </button>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default VisionEvents;
