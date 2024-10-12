import s from './authOptions.module.css';
import React from 'react';
import { useNavigate } from 'react-router-dom'; // Для навигации
import phone from '../../assets/loginIcons/phone.svg';
import facebook from '../../assets/loginIcons/facebook.svg';
import google from '../../assets/loginIcons/google.svg';
import apple from '../../assets/loginIcons/apple.svg';

const AuthOptions = () => {
  const navigate = useNavigate(); // Навигация

  const handleGoogleLogin = () => {
    // Перенаправляем на ваш API для Google аутентификации
    window.location.href = 'https://freevetback.ru/users/login/google';
  };

  const handleFacebookLogin = () => {
    // Перенаправляем на ваш API для Facebook аутентификации
    window.location.href = 'https://freevetback.ru/users/login/facebook/';
  };

  const handleAppleLogin = () => {
    alert('Apple login not implemented yet!');
  };

  const handlePhoneLogin = () => {
    navigate('/register'); // Навигация на форму
  };

  return (
    <div className={s.container}>
      <p className={s.title}>Зарегистрироваться</p>
      <div className={s.buttonGroup}>
        <button onClick={handlePhoneLogin} className={s.button}>
          <img src={phone} alt="Phone Login" className={s.icon} />
        </button>

        {/* Кастомная кнопка Facebook с перенаправлением на API */}
        <button onClick={handleFacebookLogin} className={s.button}>
          <img src={facebook} alt="Facebook Login" className={s.icon} />
        </button>

        {/* Кастомная кнопка Google с перенаправлением на API */}
        <button onClick={handleGoogleLogin} className={s.button}>
          <img src={google} alt="Google Login" className={s.icon} />
        </button>

        <button onClick={handleAppleLogin} className={s.button}>
          <img src={apple} alt="Apple Login" className={s.icon} />
        </button>
      </div>

      <div className={s.lineBox}>
        <div className={s.line}></div>
        <p>или</p>
        <div className={s.line}></div>
      </div>

      <p className={s.title}>Войти</p>
      <div className={s.buttonGroup}>
        <button onClick={handlePhoneLogin} className={s.button}>
          <img src={phone} alt="Phone Login" className={s.icon} />
        </button>

        <button onClick={handleFacebookLogin} className={s.button}>
          <img src={facebook} alt="Facebook Login" className={s.icon} />
        </button>

        <button onClick={handleGoogleLogin} className={s.button}>
          <img src={google} alt="Google Login" className={s.icon} />
        </button>

        <button onClick={handleAppleLogin} className={s.button}>
          <img src={apple} alt="Apple Login" className={s.icon} />
        </button>
      </div>
    </div>
  );
};

export default AuthOptions;
