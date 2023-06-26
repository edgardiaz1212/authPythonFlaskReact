import React, { useContext } from "react";
import { Context } from "../store/appContext";
import rigoImageUrl from "../../img/rigo-baby.jpg";
import "../../styles/home.css";
import Login from "../component/Login.jsx";

export const Home = () => {
	const { store, actions } = useContext(Context);

	return (
		<div>
      {store.token ? <p>Private</p> : <Login />}
    </div>
	);
};
