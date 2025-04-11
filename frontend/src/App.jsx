import React, { useState, useEffect } from 'react';
import SongTable from './components/SongTable';
import axios from 'axios';

const App = () => {
  const [genreFilter, setGenreFilter] = useState('');
  const [typeFilter, setTypeFilter] = useState('');
  const [surpriseSong, setSurpriseSong] = useState(null);
  const [songsData, setSongsData] = useState([]); // To store songs data fetched from Snowflake

  // Fetch data from the backend API (which queries Snowflake)
  useEffect(() => {
    axios
      .get('https://isoloops-api.vercel.app/api/query.py')// Correct API endpoint
      .then((response) => {
        console.log('Fetched data:', response.data);  // Check if data is coming through
        const rawData = response.data.samples || [];
        
        const normalized = rawData.map((sample) => ({
          ...sample,
          TITLE: sample.title,
          YOUTUBE_URL: sample.youtube_url,
          START_TIME: sample.start_time,
          END_TIME: sample.end_time,
          SAMPLE_TYPE: sample.sample_type,
          DESCRIPTION: sample.description,
          GENRE: sample.genre,
          DECADE: sample.decade,
          START_SECONDS: sample.start_seconds,
          END_SECONDS: sample.end_seconds,
          DURATION: sample.duration
        }));
        
        console.log("Normalized songs:", normalized);  // Log the normalized data
        setSongsData(normalized);
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
      });
  }, []);// Empty dependency array ensures this runs only once on component mount

  // Extract unique genres and sample types for filtering
  const genres = [...new Set(songsData.map((song) => song.GENRE))];
  const sampleTypes = [...new Set(songsData.map((song) => song.SAMPLE_TYPE))];

  // Filter songs based on genre and sample type
  const filteredSongs = surpriseSong
    ? [surpriseSong]
    : songsData.filter((song) => {
        return (
          (genreFilter === '' || song.GENRE === genreFilter) &&
          (typeFilter === '' || song.SAMPLE_TYPE === typeFilter)
        );
      });

  // Tag component for genre and sample type filters
  const Tag = ({ value, label, active, onClick, color }) => {
    const base = 'px-3 py-1 text-sm rounded-full font-medium transition';
    const classMap = {
      green: active
        ? 'bg-green-600 text-white'
        : 'bg-green-100 text-green-800 hover:bg-green-200',
      blue: active
        ? 'bg-blue-600 text-white'
        : 'bg-blue-100 text-blue-800 hover:bg-blue-200',
    };

    return (
      <button
        onClick={() => onClick(value)}
        className={`${base} ${classMap[color]}`}
      >
        {label}
      </button>
    );
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-6xl mx-auto bg-white shadow-md rounded-2xl p-6">
        <div className="flex items-center gap-3 mb-2">
          <img
            src="/isoloops-logo-transparent.png"
            alt="isoloops logo"
            className="h-10 w-10"
          />
        </div>
        <p className="text-gray-600 mb-6 italic">Find the cleanest samples in the wild.</p>

        {/* Surprise Me Button */}
        {!surpriseSong ? (
          <button
            className="mb-6 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
            onClick={() => {
              const randIndex = Math.floor(Math.random() * songsData.length);
              setSurpriseSong(songsData[randIndex]);
            }}
          >
            🎲 Surprise Me
          </button>
        ) : (
          <button
            className="mb-6 px-4 py-2 bg-gray-300 text-gray-800 rounded-lg hover:bg-gray-400 transition"
            onClick={() => setSurpriseSong(null)}
          >
            ✖️ Clear Surprise
          </button>
        )}

        {/* Filters (hidden during surprise view) */}
        {!surpriseSong && (
          <>
            <div className="mb-4">
              <p className="text-sm font-semibold mb-2">Genres:</p>
              <div className="flex flex-wrap gap-2">
                <Tag
                  value=""
                  label="All"
                  active={genreFilter === ''}
                  onClick={setGenreFilter}
                  color="green"
                />
                {genres.map((genre, idx) => (
                  <Tag
                    key={idx}
                    value={genre}
                    label={genre}
                    active={genreFilter === genre}
                    onClick={setGenreFilter}
                    color="green"
                  />
                ))}
              </div>
            </div>

            <div className="mb-6">
              <p className="text-sm font-semibold mb-2">Sample Types:</p>
              <div className="flex flex-wrap gap-2">
                <Tag
                  value=""
                  label="All"
                  active={typeFilter === ''}
                  onClick={setTypeFilter}
                  color="blue"
                />
                {sampleTypes.map((type, idx) => (
                  <Tag
                    key={idx}
                    value={type}
                    label={type.replace('_', ' ')}
                    active={typeFilter === type}
                    onClick={setTypeFilter}
                    color="blue"
                  />
                ))}
              </div>
            </div>
          </>
        )}

        {/* Table */}
        <SongTable songs={filteredSongs} /> {/* Pass filtered songs to SongTable */}
      </div>
    </div>
  );
};

export default App;