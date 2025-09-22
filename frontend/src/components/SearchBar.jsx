import { useState } from "react";
import { FaSearch } from "react-icons/fa";

export default function SearchBar({ onSearch }) {
  const [search, setSearch] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    const value = search.trim();
    onSearch(value === "" ? null : value);
  };


  return (
    <form onSubmit={handleSubmit} className="mb-6 w-full max-w-md mx-auto">
      <div className="flex w-full rounded-full border border-white bg-transparent">
        <input
          type="text"
          placeholder="Buscar ciudad..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="flex-auto px-4 py-2 text-white placeholder-white placeholder-opacity-100 bg-transparent border-none outline-none"

        />
        <button
          type="submit"
          className="flex items-center justify-center px-4 py-2 text-white bg-transparent border-none rounded-l-xl"
        >
          <FaSearch className="h-5 w-5" />
        </button>
      </div>
    </form>
  );
}