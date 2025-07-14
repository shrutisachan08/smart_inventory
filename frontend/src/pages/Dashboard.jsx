// src/pages/Dashboard.jsx

import React from "react";
import { Link } from "react-router-dom";
import { BarChart3, RefreshCcw, Leaf, Eye, MapPin } from "lucide-react";


const Dashboard = () => {
  const cards = [
   { 
     title: "Shelf Life & Expiry",
     icon: <BarChart3 className="text-blue-400" size={32} />,
     description: "Monitor products nearing expiry in real-time.",
     link: "/shelf-life-expiry",
     color: "blue-400"
    },
    {
      title: "Predictive Restocking",
      icon: <RefreshCcw className="text-green-400" size={32} />,
      description: "AI-based restock suggestions to reduce waste.",
      link: "/restocking",
      color: "green-400"
    },
    {
      title: "Eco-Friendly Tasks",
      icon: <Leaf className="text-emerald-400" size={32} />,
      description: "View eco-points and leaderboard actions.",
      link: "/eco",
      color: "emerald-400"
    },
    {
      title: "Vision Monitoring",
      icon: <Eye className="text-pink-400" size={32} />,
      description: "Get alerts from shelf vision surveillance.",
      link: "/vision-events",
      color: "pink-400"
    },
    {
     title: "Inventory Redistribution",
     icon: <RefreshCcw className="text-yellow-400" size={32} />,
     description: "Balance overstocked and understocked items across stores.",
     link: "/redistribution",
     color: "yellow-400"
    },
    {
      title: "Smart Task Assigner",
      icon: <MapPin className="text-cyan-400" size={32} />,
      description: "Assign tasks to nearest staff using geo-location.",
      link: "/assign-task",
      color: "cyan-400"
    }

  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-950 via-purple-900 to-black text-white px-6 py-16">
      <div className="text-center mb-12">
        <h1 className="text-6xl font-extrabold bg-gradient-to-r from-yellow-300 via-pink-400 to-purple-500 text-transparent bg-clip-text animate-pulse">
          🚀 Dashboard Hub
        </h1>
        <p className="mt-4 text-lg text-gray-300">
          Choose a feature module to explore inventory intelligence in action.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-8 max-w-5xl mx-auto">
        {cards.map((card) => (
          <Link
            to={card.link}
            key={card.title}
            className="bg-white/10 hover:bg-white/20 transition p-6 rounded-xl shadow-xl flex flex-col items-start gap-3"
          >
            {card.icon}
            <h2 className="text-2xl font-bold">{card.title}</h2>
            <p className="text-gray-300">{card.description}</p>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
