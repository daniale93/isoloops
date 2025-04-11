import React from 'react';
const SongTable = ({ songs }) => {
  console.log('Songs in SongTable:', songs);  // Log the songs prop to check if it's passed correctly
  return (
    <table className="w-full text-sm border-collapse">
      <thead>
        <tr className="bg-gray-200 text-left">
          <th className="p-2">Title</th>
          <th className="p-2">Sample Type</th>
          <th className="p-2">Genre</th>
          <th className="p-2">Preview</th>
          <th className="p-2">Description</th>
        </tr>
      </thead>
      <tbody>
        {songs && songs.length > 0 ? (
          songs.map((song, index) => {
            const videoId = song.YOUTUBE_URL
              ? new URL(song.YOUTUBE_URL).searchParams.get('v')
              : null;

            const start = song.START_TIME
              ? parseInt(song.START_TIME.split(':').reduce((acc, t) => 60 * acc + +t, 0))
              : 0;

            return (
              <tr key={index} className="border-t">
                <td className="p-2">{song.TITLE || 'Unknown Title'}</td>
                <td className="p-2">
                  <span className="inline-block px-2 py-1 text-xs font-medium text-white bg-blue-600 rounded-full">
                    {song.SAMPLE_TYPE ? song.SAMPLE_TYPE.replace('_', ' ') : 'Unknown Sample Type'}
                  </span>
                </td>
                <td className="p-2">
                  <span className="inline-block px-2 py-1 text-xs font-medium text-white bg-green-600 rounded-full">
                    {song.GENRE || 'Unknown Genre'}
                  </span>
                </td>
                <td className="p-2">
                  {videoId ? (
                    <iframe
                      width="200"
                      height="113"
                      src={`https://www.youtube.com/embed/${videoId}?start=${start}`}
                      title={`Sample video for ${song.TITLE || 'track'}`}   
                      frameBorder="0"
                      allowFullScreen
                    ></iframe>
                  ) : (
                    <span>No Preview</span>
                  )}
                </td>
                <td className="p-2">{song.DESCRIPTION || 'No Description'}</td>
              </tr>
            );
          })
        ) : (
          <tr>
            <td colSpan="5" className="p-2 text-center">No songs available</td>
          </tr>
        )}
      </tbody>
    </table>
  );
};
export default SongTable;