import { FaSearch } from "react-icons/fa";

export default function SearchBar() {
  return (
    <div className="mb-3 xl:w-96">
      <div className="relative mb-4 flex w-full flex-wrap items-stretch">
        {/* Input */}
        <input
          type="search"
          className="relative m-0 block flex-auto rounded-l border border-solid border-neutral-300 bg-white px-3 py-2 text-base font-normal leading-[1.6] text-neutral-700 outline-none transition duration-200 ease-in-out focus:z-[3] focus:border-blue-500 focus:shadow-[inset_0_0_0_1px_rgb(59,113,202)] dark:border-neutral-600 dark:text-neutral-200 dark:placeholder:text-neutral-400 dark:focus:border-blue-500"
          placeholder="Search"
          aria-label="Search"
        />

        {/* Icono sin fondo */}
        <button
          type="submit"
          className="flex items-center px-3 text-gray-500 hover:text-blue-600 focus:outline-none bg-transparent"
        >
          <FaSearch className="h-5 w-5" />
        </button>
      </div>
    </div>
  );
}
