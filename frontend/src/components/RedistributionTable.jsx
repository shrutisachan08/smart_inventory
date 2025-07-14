import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Download, CheckCircle } from 'lucide-react';

const RedistributionTable = () => {
  const [data, setData] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    axios.get('http://127.0.0.1:5001/redistribute')
      .then(res => setData(res.data))
      .catch(err => console.error(err));
  }, []);

  const handleExportCSV = () => {
    const headers = ['Product', 'From Store', 'To Store', 'Suggested Transfer'];
    const rows = data.map(item => [
      item.ProductName || item.Product,
      item.FromStore,
      item.ToStore,
      item.SuggestedTransfer
    ]);
    const csvContent = [headers, ...rows]
      .map(row => row.join(','))
      .join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'redistribution_suggestions.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleTransfer = (item) => {
    alert(`Initiating transfer: ${item.SuggestedTransfer} units of ${item.ProductName || item.Product} from ${item.FromStore} to ${item.ToStore}`);
  };

  const filteredData = data.filter(item =>
    (item.ProductName || '').toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-indigo-950 to-black text-white px-6 py-12">
      <div className="max-w-7xl mx-auto bg-white/10 backdrop-blur-md rounded-2xl shadow-lg p-8 border border-purple-400">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <h2 className="text-4xl font-extrabold text-purple-200 tracking-wide">
            🔄 Inventory Redistribution Suggestions
          </h2>
          <div className="flex gap-2">
            <input
            
              type="text"
              placeholder="Search product..."
              className="border px-4 py-2 rounded-lg text-white"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            <button
              onClick={handleExportCSV}
              className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg flex items-center gap-2"
            >
              <Download size={18} /> Export CSV
            </button>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="min-w-full text-sm text-white text-left border border-purple-500 rounded-lg">
            <thead className="bg-purple-700 text-white text-base">
              <tr>
                <th className="px-4 py-3 border border-purple-500">📦 Product</th>
                <th className="px-4 py-3 border border-purple-500">🏬 From Store</th>
                <th className="px-4 py-3 border border-purple-500">🏪 To Store</th>
                <th className="px-4 py-3 border border-purple-500">🔢 Transfer Qty</th>
                <th className="px-4 py-3 border border-purple-500">⚙️ Action</th>
              </tr>
            </thead>
            <tbody>
              {filteredData.map((item, idx) => (
                <tr key={idx} className="hover:bg-white/10 transition-all duration-200">
                  <td className="px-4 py-3 border border-purple-600">{item.ProductName || item.Product}</td>
                  <td className="px-4 py-3 border border-purple-600">{item.FromStore}</td>
                  <td className="px-4 py-3 border border-purple-600">{item.ToStore}</td>
                  <td className="px-4 py-3 border border-purple-600 font-semibold text-purple-300">
                    {item.SuggestedTransfer}
                  </td>
                  <td className="px-4 py-3 border border-purple-600">
                    <button
                      onClick={() => handleTransfer(item)}
                      className="bg-emerald-600 hover:bg-emerald-700 text-white px-3 py-1 rounded flex items-center gap-1"
                    >
                      <CheckCircle size={16} /> Transfer
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <p className="text-sm text-purple-300 mt-6 text-center italic">
          These transfers help balance inventory across stores and reduce product wastage.
        </p>
      </div>
    </div>
  );
};

export default RedistributionTable;