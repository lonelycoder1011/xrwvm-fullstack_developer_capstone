import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';

const PostReview = () => {
  const navigate = useNavigate();
  const [dealer, setDealer] = useState({});
  const [review, setReview] = useState("");
  const [model, setModel] = useState("");
  const [year, setYear] = useState("");
  const [date, setDate] = useState("");
  const [carmodels, setCarmodels] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const { id } = useParams();
  const curr_url = window.location.href;
  const root_url = curr_url.substring(0, curr_url.indexOf("postreview"));
  
  // Corrected endpoints
  const dealer_url = `${root_url}djangoapp/dealer/${id}`;
  const review_url = `${root_url}djangoapp/postreview/${id}`; // Added dealer_id in URL
  const carmodels_url = `${root_url}djangoapp/get_cars`;

  const postreview = async () => {
    try {
      setError("");
      setLoading(true);

      if (!model || !review || !date || !year) {
        setError("All fields are mandatory");
        return;
      }

      const name = [sessionStorage.getItem("firstname"), sessionStorage.getItem("lastname")]
        .filter(Boolean).join(" ") || sessionStorage.getItem("username");

      const [make_chosen, ...modelParts] = model.split(" ");
      const model_chosen = modelParts.join(" ");

      const response = await fetch(review_url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${sessionStorage.getItem('token')}`
        },
        body: JSON.stringify({
          name,
          dealership: id,
          review,
          purchase: true,
          purchase_date: date,
          car_make: make_chosen,
          car_model: model_chosen,
          car_year: year,
        }),
      });

      const data = await response.json();
      if (data.status === 200) {
        navigate(`/dealer/${id}`);
      } else {
        setError(data.message || "Failed to post review");
      }
    } catch (err) {
      setError("Network error. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const get_dealer = async () => {
    try {
      const res = await fetch(dealer_url);
      const data = await res.json();
      if (data.status === 200 && data.dealer?.length > 0) {
        setDealer(data.dealer[0]);
      }
    } catch (err) {
      setError("Failed to load dealer information");
    }
  };

  const get_cars = async () => {
    try {
      const res = await fetch(carmodels_url);
      const data = await res.json();
      if (data.CarModels) {
        setCarmodels(Array.isArray(data.CarModels) ? data.CarModels : []);
      }
    } catch (err) {
      setError("Failed to load car models");
    }
  };

  useEffect(() => {
    get_dealer();
    get_cars();
  }, [id]); // Added id to dependency array

  return (
    <div>
      <Header />
      <div style={{ margin: "5%" }}>
        <h1 style={{ color: "darkblue" }}>{dealer.full_name || "Dealer"}</h1>
        
        {error && <div className="error-message">{error}</div>}

        <textarea 
          id='review' 
          cols='50' 
          rows='7' 
          value={review}
          onChange={(e) => setReview(e.target.value)}
          placeholder="Write your review here..."
        />

        <div className='input_field'>
          <label>Purchase Date</label>
          <input 
            type="date" 
            value={date}
            max={new Date().toISOString().split('T')[0]}
            onChange={(e) => setDate(e.target.value)}
          />
        </div>

        <div className='input_field'>
          <label>Car Model</label>
          <select 
            value={model}
            onChange={(e) => setModel(e.target.value)}
            required
          >
            <option value="" disabled>Choose Car</option>
            {carmodels.map((carmodel, index) => (
              <option 
                key={index} 
                value={`${carmodel.CarMake} ${carmodel.CarModel}`}
              >
                {carmodel.CarMake} {carmodel.CarModel}
              </option>
            ))}
          </select>        
        </div>

        <div className='input_field'>
          <label>Car Year</label>
          <input 
            type="number" 
            value={year}
            min="1900" 
            max={new Date().getFullYear()}
            onChange={(e) => setYear(e.target.value)}
          />
        </div>

        <div>
          <button 
            className='postreview' 
            onClick={postreview}
            disabled={loading}
          >
            {loading ? "Posting..." : "Post Review"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default PostReview;