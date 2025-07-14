import React, { useEffect, useState } from "react";

const ShelfLifeExpiry = () => {
  const [items, setItems] = useState([]);  // ✅ State for fetched data
  const [loading, setLoading] = useState(true);  // ✅ Loading state

  useEffect(() => {
    fetch("http://localhost:5000/api/check-expiry")
      .then((res) => res.json())
      .then((data) => {
        console.log("Fetched data:", data);  // ✅ Log response from backend
        setItems(data);                      // ✅ Save to state
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching expiry data:", err);
        setLoading(false);
      });
  }, []);

  console.log("Items in state:", items);  // ✅ Log items before rendering

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-black text-white px-6 py-12">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 text-center text-blue-400">
          🧪 Shelf Life & Expiry Monitoring
        </h1>

        {loading ? (
          <p className="text-center text-gray-300">Loading expiry data...</p>
        ) : items.length === 0 ? (
          <p className="text-center text-gray-300">No expiring products found.</p>
        ) : (
          <div className="overflow-x-auto bg-white/10 p-4 rounded-xl">
            <table className="min-w-full text-sm">
              <thead>
                <tr className="text-left text-blue-300 border-b border-white/20">
                  <th className="p-2">Product</th>
                  <th className="p-2">Store</th>
                  <th className="p-2">Category</th>
                  <th className="p-2">Expiry Date</th>
                  <th className="p-2">Quantity</th>
                  <th className="p-2">Status</th>
                </tr>
              </thead>
              <tbody>
                {items.map((data) => (
                  <tr key={data._id || data.ProductID} className="hover:bg-white/5">
                    <td className="p-2">{data.ProductName}</td>
                    <td className="p-2">{data.StoreID}</td>
                    <td className="p-2">{data.Category}</td>
                    <td className="p-2">
                      {new Date(data.ExpiryDate).toLocaleDateString()}
                    </td>
                    <td className="p-2">{data.QuantityInStock}</td>
                    <td className="p-2">
                      <span
                        className={`px-2 py-1 rounded-full text-xs font-medium ${
                          data.Status === "Expired"
                            ? "bg-red-500 text-white"
                            : data.Status === "Nearing Expiry"
                            ? "bg-yellow-400 text-black"
                            : "bg-green-500 text-white"
                        }`}
                      >
                        {data.Status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default ShelfLifeExpiry;
