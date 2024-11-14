import React from 'react'

{/* className="flex justify-center" */}
const LogIn = () => {
  return (
    <div>
        <div className="flex justify-center bg-custom-pattern bg-cover bg-center min-h-screen">
            <section>
                <form className=" bg-white border border-gray-300 p-6 rounded-lg shadow-md w-full max-w-xs mt-40 mr-10">
                    <h2 className="text-2xl font-bold mb-6 text-center">FlipShare</h2>
                    <div className="mb-4">
                        <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="username">
                            Username
                        </label>
                        <input
                            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                            id="username"
                            type="text"
                            placeholder="Username"
                        />
                    </div>
                    <div className="mb-6">
                        <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
                            Password
                        </label>
                        <input
                            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
                            id="password"
                            type="password"
                            placeholder="******************"
                        />
                    </div>
                    <div className="flex items-center ml-6 mb-4 ">
                        <button
                            className="mr-5 bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded focus:outline-none focus:shadow-outline"
                            type="button"
                        >
                            Sign In
                        </button>
                        <button
                            className="bg-green-500 hover:bg-green-700 text-white font-bold py-3 px-6 rounded focus:outline-none focus:shadow-outline"
                            type="button"
                        >
                            Sign Up
                        </button>
                    </div>
                    <div className="border-t border-gray-300 my-4"></div>
                    <div className="flex items-center justify-center">
                        <button
                            className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-3 px-6 rounded focus:outline-none focus:shadow-outline"
                            type="button"
                        >
                            Sign in with SSO
                        </button>
                    </div>
                </form>
            </section>
        </div>
    </div>
  )
}

export default LogIn