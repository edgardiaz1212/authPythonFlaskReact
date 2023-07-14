import React, { useContext, useState } from "react";
import { Context } from "../store/appContext";

const Private = () => {
  
  const {store} = useContext(Context)
    
  if (!store.token) {
    return <div>You must be logged in to access this page.</div>;
  }

  return (
    <div>
      <h1>Private</h1>
      <h2>Only logged-in users</h2>
    </div>
  );
};

export default Private;