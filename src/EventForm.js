import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './EventForm.css';

const EventForm = ({ onCreate }) => {
  const [title, setTitle] = useState('');
  const [details, setDetails] = useState('');
  const [datetime, setDatetime] = useState('');
  const [location, setLocation] = useState('');
  const navigate = useNavigate();

  const handleCreateEvent = (e) => {
    e.preventDefault();
    fetch(`${process.env.REACT_APP_API_BASE_URL}/api/events`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        title: title,
        details: details,
        datetime: datetime,
        location: location,
      }),
    })
    .then(response => response.json())
    .then(data => {
      if (data.message === 'Event created successfully') {
        onCreate(data);
        setTitle('');
        setDetails('');
        setDatetime('');
        setLocation('');
      } else {
        alert('Failed to create event');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Failed to create event');
    });
  };

  const handleLogout = () => {
    navigate('/login');
  };

  return (
    <div className="event-form-container">
      <form onSubmit={handleCreateEvent}>
        <div className="form-row">
          <div className="form-column">
            <div className="input-group">
              <label>Title</label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
              />
            </div>
            <div className="input-group">
              <label>Details</label>
              <textarea
                value={details}
                onChange={(e) => setDetails(e.target.value)}
                required
              ></textarea>
            </div>
          </div>
          <div className="form-column">
            <div className="input-group">
              <label>Date and Time</label>
              <input
                type="datetime-local"
                value={datetime}
                onChange={(e) => setDatetime(e.target.value)}
                required
              />
            </div>
            <div className="input-group">
              <label>Location</label>
              <input
                type="text"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                required
              />
            </div>
          </div>
        </div>
        <div className="button-row">
          <button type="submit" className="btn create-event-btn">Create Event</button>
          <button className="btn logout-btn" onClick={handleLogout}>Logout</button>
        </div>
      </form>
    </div>
  );
};

export default EventForm;