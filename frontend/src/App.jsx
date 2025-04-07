import React, { useState } from 'react';
import SongTable from './components/SongTable';
import sampleData from './data/songs.json';

const App = () => {
  const [genreFilter, setGenreFilter] = useState('');
  const [typeFilter, setTypeFilter] = useState('');
  const [surpriseSong, setSurpriseSong] = useState(null);

  const genres = [...new Set(sampleData.map(song => song.genre))];
  const sampleTypes = [...new Set(sampleData.map(song => song.sample_type))];

  const filteredSongs = surpriseSong
    ? [surpriseSong]
    : sampleData.filter(song => {
        return (
          (genreFilter === '' || song.genre === genreFilter) &&
          (typeFilter === '' || song.sample_type === typeFilter)
        );
      });

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
        <h1 className="text-3xl font-extrabold text-gray-800 mb-1">isoloops</h1>
        <p className="text-gray-600 mb-6 italic">Find the cleanest samples in the wild.</p>

        {/* Surprise Me Button */}
        {!surpriseSong ? (
          <button
            className="mb-6 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
            onClick={() => {
              const randIndex = Math.floor(Math.random() * sampleData.length);
              setSurpriseSong(sampleData[randIndex]);
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
                <Tag value="" label="All" active={genreFilter === ''} onClick={setGenreFilter} color="green" />
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
                <Tag value="" label="All" active={typeFilter === ''} onClick={setTypeFilter} color="blue" />
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
        <SongTable songs={filteredSongs} />
      </div>
    </div>
  );
};

export default App;