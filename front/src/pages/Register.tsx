import React, { useState } from "react";
import axios, { AxiosError } from "axios";

const Register: React.FC = () => {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage("");

    try {
      const resp = await axios.post(
        `${import.meta.env.VITE_API_URL}/api/register`,
        { login, password }
      );
      setMessage(resp.data.message); 
    } catch (error) {
      const err = error as AxiosError<any>;

      if (err.response) {
        const status = err.response.status;
        const data = err.response.data as any;

        if (status === 409) {
          setMessage("Логин уже занят");
        } else if (status === 422) {
            const detail = (data as any)?.detail;

            if (typeof detail === "string") {
                // наши ошибки пароля ("Пароль: минимум 8 символов", и т.д.)
                setMessage(detail);
            } else if (Array.isArray(detail) && detail.length > 0) {
                // классический формат Pydantic: [{msg: "..."}]
                const msg = detail.map((d: any) => d.msg).join("; ");
                setMessage(msg);
            } else {
                setMessage("Данные не прошли валидацию");
            }
         }
        }
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>Регистрация</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Логин</label>
          <input
            value={login}
            onChange={(e) => setLogin(e.target.value)}
            placeholder="login"
          />
        </div>
        <div>
          <label>Пароль</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Пароль"
          />
        </div>
        <button type="submit">Зарегистрироваться</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default Register;
