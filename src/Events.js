import React, { useEffect, useState } from 'react';
import './Events.css';
import EventForm from './EventForm';

const Events = () => {
  const [events, setEvents] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const eventsPerPage = 5;

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = () => {
    fetch(`${process.env.REACT_APP_API_BASE_URL}/api/events`)
      .then(response => response.json())
      .then(data => {
        data.sort((a, b) => new Date(a.datetime) - new Date(b.datetime));
        setEvents(data);
      })
      .catch(error => {
        console.error('Error fetching events:', error);
      });
  };

  const handleCreateEvent = (newEvent) => {
    fetchEvents();
    setEvents([...events, newEvent]);
  };

  const handleNextPage = () => {
    if (currentIndex + eventsPerPage < events.length) {
      setCurrentIndex(currentIndex + 1);
    }
  };

  const handlePreviousPage = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  const displayedEvents = events.slice(currentIndex, currentIndex + eventsPerPage);

  return (
    <div className="events-container">
      <EventForm onCreate={handleCreateEvent} />

      <h2>Events</h2>
      <div className="events-list">
        {displayedEvents.map(event => {
          const eventDate = new Date(event.datetime);
          const formattedDate = eventDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }).toUpperCase();
          const formattedTime = eventDate.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });

          return (
            <div key={event.id} className="event-item">
              <p className="event-date">{formattedDate}</p>
              <p className="event-time">{formattedTime}</p>
              <h3>{event.title}</h3>
              <p>{event.details}</p>
              <p>{event.location}</p>
            </div>
          );
        })}
      </div>
      <div className="pagination">
        <button onClick={handlePreviousPage} disabled={currentIndex === 0}>Previous</button>
        <button onClick={handleNextPage} disabled={currentIndex + eventsPerPage >= events.length}>Next</button>
      </div>
    </div>
  );
};

export default Events;