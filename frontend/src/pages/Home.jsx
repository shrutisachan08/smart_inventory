import React from "react";
import { Link } from "react-router-dom";

const Home = () => {
  const features = [
    {
      title: "📦 Shelf Life & Expiry Monitoring",
      howToUse: "Upload your inventory or connect real-time sensors to monitor expiry dates. System auto-checks daily.",
      benefits: "Reduces spoilage and waste, ensures timely clearance, boosts customer safety.",
    },
    {
      title: "🔁 Predictive Restocking with AI",
      howToUse: "System analyzes current stock and forecasted demand. Click '+' to add suggestions to purchase list.",
      benefits: "Minimizes out-of-stock & overstock, ensures smart planning, improves supply chain.",
    },
    {
      title: "🌿 Eco-Friendly Staff Tasks",
      howToUse: "System tags organic/eco items and assigns them to nearby staff based on aisles & store.",
      benefits: "Promotes sustainability, rewards responsible staff, improves eco brand image.",
    },
    {
      title: "👁️ Vision-Based Event Tracking",
      howToUse: "Simulate camera-based events like 'item picked' or 'suspicious activity'. Alerts are logged instantly.",
      benefits: "Improves surveillance, boosts shelf activity tracking, enhances store security.",
    },
    {
      title: "🧭 Smart Staff Routing",
      howToUse: "System fetches pending tasks & assigns routes to staff within same shift using aisle data.",
      benefits: "Improves efficiency, reduces idle time, smart distribution of workload.",
    },
    {
      title: "🛰️ Task Assignment via Location",
      howToUse: "Input task coordinates & description. Nearest available staff is auto-assigned in real-time.",
      benefits: "Leverages real-time location, improves responsiveness, ensures faster issue resolution.",
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-950 via-purple-900 to-black text-white px-6 py-16">
      <div className="text-center mb-12">
        <h1 className="text-6xl font-extrabold bg-gradient-to-r from-yellow-300 via-pink-400 to-purple-500 text-transparent bg-clip-text animate-pulse">
          🧠 SmartInventory
        </h1>
        <p className="mt-4 text-lg text-gray-300">
          Explore features built for intelligent retail automation and smarter inventory.
        </p>
      </div>

      {/* Feature Cards */}
      <div className="space-y-8 max-w-4xl mx-auto">
        {features.map((feature, idx) => (
          <div
            key={idx}
            className="bg-white/10 hover:bg-white/20 transition rounded-xl shadow-xl p-6 space-y-3"
          >
            <h2 className="text-2xl font-bold text-yellow-300">{feature.title}</h2>
            <p className="text-gray-300">
              <span className="font-semibold text-teal-400">How to Use:</span> {feature.howToUse}
            </p>
            <p className="text-gray-300">
              <span className="font-semibold text-green-400">Benefits:</span> {feature.benefits}
            </p>
          </div>
        ))}
      </div>

      {/* Dashboard Launch Button */}
      <div className="text-center mt-16">
        <Link
          to="/dashboard"
          className="inline-block bg-gradient-to-r from-purple-500 to-pink-500 hover:from-yellow-400 hover:to-pink-400 text-white text-xl font-semibold px-8 py-3 rounded-full shadow-lg transition transform hover:scale-105"
        >
          🚀 Launch Dashboard
        </Link>
      </div>
    </div>
  );
};

export default Home;
