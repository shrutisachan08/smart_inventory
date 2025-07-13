import React, { useEffect, useState } from "react";
import axios from "axios";
import { FaPlus, FaTrash } from "react-icons/fa";

const PredictiveRestocking = () => {
  const [suggestions, setSuggestions] = useState([]);
  const [selectedItems, setSelectedItems] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:5000/api/restock/recommendations")
      .then((res) => {
        if (res.data?.data?.Items) {
          setSuggestions(res.data.data.Items);
        }
      })
      .catch((err) => console.error("Error fetching restock data", err));
  }, []);

  const handleAddItem = (item) => {
    if (!selectedItems.find((i) => i.ProductID === item.ProductID)) {
      setSelectedItems([...selectedItems, item]);
    }
  };

  const handleRemoveItem = (productId) => {
    setSelectedItems(selectedItems.filter((item) => item.ProductID !== productId));
  };

  return (
    <div className="bg-gradient-to-b from-purple-50 via-grey to-purple-100 min-h-screen p-6 font-sans">
      <h2 className="text-4xl font-extrabold text-purple-600 mb-6 drop-shadow">
        🔮 Predictive Restocking Assistant
      </h2>

      {suggestions.length === 0 ? (
        <p className="text-gray-600 text-lg font-medium">
          No restocking suggestions available at this moment.
        </p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {suggestions.map((item) => (
            <div
              key={item.ProductID}
              className="bg-white border-2 border-purple-200 rounded-xl p-5 shadow-md hover:shadow-lg transition-all duration-300"
            >
              <h3 className="text-2xl font-bold text-purple-600 mb-1">
                {item.ProductName}
              </h3>
              <p className="text-sm text-gray-700 mb-1">
                <strong className="text-purple-600">Category:</strong>{" "}
                {item.Category}
              </p>
              <p className="text-sm text-gray-700 mb-1">
                <strong className="text-purple-600">Current Stock:</strong>{" "}
                {item.CurrentStock}
              </p>
              <p className="text-sm text-gray-700 mb-1">
                <strong className="text-purple-600">Forecasted Demand:</strong>{" "}
                {item.ForecastedDemand}
              </p>
              <p className="text-sm text-gray-700 mb-3">
                <strong className="text-purple-600">Units To Order:</strong>{" "}
                <span className="font-semibold text-purple-800 text-lg">
                  {item.UnitsToOrder}
                </span>
              </p>

              <button
                onClick={() => handleAddItem(item)}
                className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700 flex items-center justify-center text-sm font-semibold"
              >
                <FaPlus className="mr-2" />
                Add to Order List
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Floating Cart List */}
      {selectedItems.length > 0 && (
        <div className="fixed top-20 right-4 w-80 bg-white shadow-xl border-4 border-purple-400 rounded-lg p-4 z-50 max-h-[80vh] overflow-y-auto">
          <h4 className="text-xl font-bold text-purple-900 mb-3 border-b pb-2">
            🧾 Order Summary
          </h4>

          {selectedItems.map((item) => (
            <div
              key={item.ProductID}
              className="flex justify-between items-start bg-purple-50 border border-purple-200 rounded p-3 mb-3"
            >
              <div>
                <p className="font-semibold text-gray-800">{item.ProductName}</p>
                <p className="text-xs text-gray-600">Qty: {item.UnitsToOrder}</p>
              </div>
              <button
                onClick={() => handleRemoveItem(item.ProductID)}
                className="text-red-600 hover:text-red-800"
              >
                <FaTrash />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default PredictiveRestocking;
