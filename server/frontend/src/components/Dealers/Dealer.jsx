import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import positive_icon from "../assets/positive.png";
import neutral_icon from "../assets/neutral.png";
import negative_icon from "../assets/negative.png";
import review_icon from "../assets/reviewbutton.png";
import Header from '../Header/Header';

const Dealer = () => {
  const [dealer, setDealer] = useState({});
  const [reviews, setReviews] = useState([]);
  const [unreviewed, setUnreviewed] = useState(false);
  const [postReview, setPostReview] = useState(<></>);

  const { id } = useParams();
  const curr_url = window.location.href;
  const root_url = curr_url.substring(0, curr_url.indexOf("dealer"));
  
  // Updated URL construction
  const dealer_url = `${root_url}djangoapp/dealer/${id}`;
  const reviews_url = `${root_url}djangoapp/reviews/dealer/${id}`;
  const post_review = `${root_url}postreview/${id}`;

  // Updated get_dealer function with proper headers
  const get_dealer = async () => {
    try {
      const res = await fetch(dealer_url, {
        method: "GET",
        headers: { 'Content-Type': 'application/json' }
      });
      
      if (res.ok) {
        const response = await res.json();
        // Handle both response formats
        if (response.dealer) {
          setDealer(response.dealer); // Directly use the dealer object
        } else if (response.status === 404) {
          console.error("Dealer not found");
        }
      }
    } catch (error) {
      console.error("Dealer fetch error:", error);
    }
  };

  const get_reviews = async () => {
    try {
      const res = await fetch(reviews_url, {
        method: "GET",
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      });
      
      if (res.ok) {
        const retobj = await res.json();
        if (retobj.reviews?.length > 0) {
          setReviews(retobj.reviews);
        } else {
          setUnreviewed(true);
        }
      }
    } catch (error) {
      console.error("Error fetching reviews:", error);
    }
  };

  const senti_icon = (sentiment) => {
    return sentiment === "positive" 
      ? positive_icon 
      : sentiment === "negative" 
        ? negative_icon 
        : neutral_icon;
  };

  useEffect(() => {
    get_dealer();
    get_reviews();
    
    if (sessionStorage.getItem("username")) {
      setPostReview(
        <a href={post_review}>
          <img
            src={review_icon}
            style={{ width: "10%", marginLeft: "10px", marginTop: "10px" }}
            alt="Post Review"
          />
        </a>
      );
    }
  }, [id]); // Removed BASE_URL from dependencies as we're using relative URLs

  return (
    <div style={{ margin: "20px" }}>
      <Header />
      <div style={{ marginTop: "10px" }}>
        <h1 style={{ color: "grey" }}>
          {dealer.full_name || dealer.short_name || "Dealer Name"}
          {postReview}
        </h1>
        <h4 style={{ color: "grey" }}>
          {dealer.city && `${dealer.city}, `}
          {dealer.address && `${dealer.address}, `}
          {dealer.zip && `Zip - ${dealer.zip}, `}
          {dealer.state || ""}
        </h4>
      </div>
      
      <div className="reviews_panel">
        {reviews.length === 0 && !unreviewed ? (
          <text>Loading Reviews...</text>
        ) : unreviewed ? (
          <div>No reviews yet! Be the first to review.</div>
        ) : (
          reviews.map((review) => (
            <div className="review_panel" key={review.id || review._id}>
              <img
                src={senti_icon(review.sentiment?.toLowerCase())}
                className="emotion_icon"
                alt="Sentiment"
              />
              <div className="review">
                {review.review || 'No review text available'}
              </div>
              <div className="reviewer">
                {review.name || "Anonymous"} - 
                {review.car_make || "Unknown Make"} 
                {review.car_model || "Unknown Model"} 
                {review.car_year || "Unknown Year"}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Dealer;