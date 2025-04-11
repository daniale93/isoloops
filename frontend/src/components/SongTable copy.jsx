import React from 'react';


const SongTable = ({ songs, highlightedId }) => {
  return (
    <table className="w-full text-sm border-collapse">
      <thead>
        <tr className="bg-gray-200 text-left">
          <th className="p-2">Title</th>
          <th className="p-2">Sample Type</th>
          <th className="p-2">Preview</th>
          <th className="p-2">Description</th>
        </tr>
      </thead>
      <tbody>
        {songs.map((song, index) => {
          const videoId = new URL(song.youtube_url).searchParams.get("v");
          const start = parseInt(song.start_time.split(":").reduce((acc, t) => 60 * acc + +t, 0));
          const rowId = `song-${index}`;

          return (
            <tr
              key={index}
              id={rowId}
              className={`border-t ${song.id === highlightedId ? 'bg-yellow-100' : ''}`}
            >
              <td className="p-2">{song.title}</td>
              <td className="p-2">
                <span className="inline-block px-2 py-1 text-xs font-medium text-white bg-blue-600 rounded-full">
                  {song.sample_type.replace('_', ' ')}
                </span>
              </td>
              <td className="p-2">
                <span className="inline-block px-2 py-1 text-xs font-medium text-white bg-green-600 rounded-full">
                  {song.genre}
                </span>
              </td>
              <td className="p-2">
                <iframe
                  width="200"
                  height="113"
                  src={`https://www.youtube.com/embed/${videoId}?start=${start}`}
                  frameBorder="0"
                  allowFullScreen
                ></iframe>
              </td>
              <td className="p-2">{song.description}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
};
export default SongTable;


