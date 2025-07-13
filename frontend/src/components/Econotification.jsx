import React, { useEffect, useState } from "react";

const EcoNotification = () => {
  const [assignments, setAssignments] = useState([]);
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:5000/api/eco/notify")
      .then((res) => res.json())
      .then((data) => {
        console.log("Fetched eco notification data:", data);
        setAssignments(data.data?.EcoAssignments || []);
        setLeaderboard(data.data?.Leaderboard || []);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Eco fetch error:", err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-900 via-emerald-800 to-black text-white px-6 py-12">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold mb-10 text-center text-green-400">
          🌱 Eco-Friendly Product Assignments
        </h1>

        {loading ? (
          <p className="text-center text-gray-300">Loading eco data...</p>
        ) : (
          <>
            {/* 📋 Assignments */}
            <div className="mb-12">
              <h2 className="text-2xl font-semibold mb-4 text-lime-300">📋 Assignments</h2>
              {assignments.length === 0 ? (
                <p className="text-gray-400">No assignments available.</p>
              ) : (
                <div className="overflow-x-auto bg-white/10 p-4 rounded-xl">
                  <table className="min-w-full text-sm">
                    <thead>
                      <tr className="text-left text-green-300 border-b border-white/20">
                        <th className="p-2">Staff</th>
                        <th className="p-2">Product</th>
                        <th className="p-2">Eco Tag</th>
                      </tr>
                    </thead>
                    <tbody>
                      {assignments.map((a, idx) => (
                        <tr key={idx} className="hover:bg-white/5">
                          <td className="p-2">{a.StaffName} ({a.StaffID})</td>
                          <td className="p-2">{a.ProductName} ({a.ProductID})</td>
                          <td className="p-2">
                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                              a.EcoTag === "Organic"
                                ? "bg-green-500 text-white"
                                : a.EcoTag === "Vegan"
                                ? "bg-yellow-400 text-black"
                                : "bg-blue-500 text-white"
                            }`}>
                              {a.EcoTag}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>

            {/* 🏆 Leaderboard */}
            <div>
              <h2 className="text-2xl font-semibold mb-4 text-lime-300">🏆 Leaderboard</h2>
              {leaderboard.length === 0 ? (
                <p className="text-gray-400">No leaderboard data available.</p>
              ) : (
                <div className="overflow-x-auto bg-white/10 p-4 rounded-xl">
                  <table className="min-w-full text-sm">
                    <thead>
                      <tr className="text-left text-green-300 border-b border-white/20">
                        <th className="p-2">Staff</th>
                        <th className="p-2">Eco Points</th>
                      </tr>
                    </thead>
                    <tbody>
                      {leaderboard.map((entry, idx) => (
                        <tr key={idx} className="hover:bg-white/5">
                          <td className="p-2">{entry.StaffName} ({entry.StaffID})</td>
                          <td className="p-2">{entry.EcoPoints}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default EcoNotification;
