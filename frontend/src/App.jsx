import { useEffect, useState } from "react";
import axios from "axios";

const API = "http://192.168.49.2:30009";

function App() {
  const [name, setName] = useState("");
  const [users, setUsers] = useState([]);

  const loadUsers = () => {
    axios.get(`${API}/users`)
      .then(res => setUsers(res.data));
  };

  const addUser = () => {
    axios.post(`${API}/users`, { name })
      .then(() => {
        setName("");
        loadUsers();
      });
  };

  useEffect(() => {
    loadUsers();
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>DevOps App</h1>

      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Enter name"
      />

      <button onClick={addUser}>Submit</button>

      <h2>Users:</h2>
      <ul>
        {users.map((u, i) => (
          <li key={i}>{u[0]}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
