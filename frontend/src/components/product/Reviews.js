import React, { useState } from 'react';

const Reviews = ({ items }) => {
  const [showAll, setShowAll] = useState(false);

  if (!items || items.length === 0) {
    return (
      <section className="card reviews">
        <h2>Customer Reviews</h2>
        <p className="no-reviews">No reviews available yet.</p>
      </section>
    );
  }

  const displayedReviews = showAll ? items : items.slice(0, 3);

  const renderStars = (rating) => {
    return Array.from({ length: 5 }, (_, index) => (
      <span key={index} className={`star ${index < rating ? 'filled' : ''}`}>
        ★
      </span>
    ));
  };

  return (
    <section className="card reviews">
      <h2>Customer Reviews</h2>
      <div className="reviews-list">
        {displayedReviews.map((review, index) => (
          <div key={index} className="review-item">
            <div className="review-header">
              <div className="reviewer-info">
                <strong>{review.reviewer_name}</strong>
                <div className="rating">
                  {renderStars(review.rating)}
                  <span className="rating-text">({review.rating}/5)</span>
                </div>
              </div>
              <span className="review-date">{review.date}</span>
            </div>
            <p className="review-text">{review.comment}</p>
            {review.helpful_count && (
              <div className="review-helpful">
                <span>{review.helpful_count} people found this helpful</span>
              </div>
            )}
          </div>
        ))}
      </div>
      {items.length > 3 && (
        <button 
          className="btn-secondary"
          onClick={() => setShowAll(!showAll)}
        >
          {showAll ? 'Show Less' : `Show All ${items.length} Reviews`}
        </button>
      )}
    </section>
  );
};

export default Reviews;