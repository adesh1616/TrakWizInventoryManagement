
import React, { useEffect } from "react";


const App = () => {
  const[message, setMessage] = useSatte("");

  const getWelcomeMessage = async () =>{
    const requestOptions = {
      method: "GEt",
      Headers: {
        "Content-Type": "application/json",
      },
    };
    const response = await fetch("/api", requestOptions);
    const data = response.json();

    console.log(data);
  };
  useEffect(()=> { getWelcomeMessage(); 
  }
  ,
  []);
  
  return (
    <div>
      <h1>Hello World</h1>
    </div>
     
  );
}

export default App;
