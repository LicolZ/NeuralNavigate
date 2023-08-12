// NeuralNavivate/my_app/src/user/userUtils.jsx

import React from 'react';

export const signOut = (setUser) => {
    // Remove token and user email from local storage
    localStorage.removeItem('token');
    localStorage.removeItem('userEmail');
    // Reset the user state
    setUser(null);
    // Optionally: Inform the backend to invalidate the token (if needed)
    // You may need to make an axios request here.
  };

export const renderUserButton = (user, handleOpen, toggleDropdown, showDropdown, signOut, setUser) => {
    if (user && user.email) {
      const displayEmail = user.email.split('@')[0];
      return (
        <>
          <button id="usernameDropdownButton" onClick={toggleDropdown}>
            {displayEmail}
          </button>
          {showDropdown && (
            <>
              <div className="dropdown-content">
                <button id="closeDropdownButton" onClick={toggleDropdown}>X</button> {/* Added Close button */}
                <div className="dropdown-items">
                  <button onClick={() => { /* go to My Profile */ }}>My Profile</button>
                  <button onClick={() => { /* go to Saved Graphs */ }}>Saved Graphs</button>
                  <button onClick={() => { signOut(setUser) }}>Sign Out →</button>
                </div>
              </div>
            </>
          )}
        </>
      );
    } else {
      return <div id="loginButton" onClick={handleOpen}>Sign In</div>;
    }
  };

  
  

  
  