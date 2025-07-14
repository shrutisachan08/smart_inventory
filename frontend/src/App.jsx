/// src/App.jsx
import React from "react";
import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home"; // or wherever your Home.jsx is
import Dashboard from "./pages/Dashboard";
import ShelfLifeExpiry from "./components/Shelf_life_expiry";
import EcoNotification from "./components/Econotification";
import PredictiveRestocking from "./components/PredictiveRestocking";
import VisionEvents from "./components/VisionEvents";
import RedistributionCards from "./components/RedistributionTable";
import AssignTask from "./components/Smart_staff";
// Add other pages if needed

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/shelf-life-expiry" element={<ShelfLifeExpiry />} />
      <Route path="/eco" element={<EcoNotification />} />
      <Route path="/restocking" element={<PredictiveRestocking />} />
      <Route path="/vision-events" element={<VisionEvents />} />
      <Route path="/redistribution" element={<RedistributionCards />} />
       <Route path="/assign-task" element={<AssignTask />} /> 

    </Routes>
  );
};

export default App;
