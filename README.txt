# **EDfilms**

EDfilms is an online platform dedicated to streaming movies. We offer a wide range of films across various genres to cater to all our users' preferences.

### **Key Features**

- Extensive movie library: Access a vast collection of films, from the latest releases to timeless classics.
- Easy navigation: Intuitive and user-friendly interface to make browsing and selecting movies a simple and enjoyable experience.
- Personalized recommendations: Advanced recommendation systems to suggest movies based on user preferences.
- Video quality: Support for various resolutions to provide the best viewing experience possible.
  
### **How to Use the WEBPAGES:**

1. Registration/Login: Create an account or log in using existing credentials.
2. Explore the library: Use the search bar or browse through genres to find the desired film.
3. Selection and playback: Once you find the film, select it to start playback.

### **How to Use the SERVER:**

1. Download Docker and docker-compose.yml.
2. Then go to a folder and go to the powershell and type the command docker-compose up.
3. If you give it enough time it will create 3 new folder one for mysql one for nginx and the last one for python.
4. If you want to check my sql's tables you can go to the powershell and use these commands.

```bash

{
docker exec -it reti_uni-mysql-1 /bin/bash
mysql -u root -p
root
USE tech
SHOW TABLES; # it will show you the tables of the sql the same can be done on the image of mysql on docker you just need to go on exec
}
```

### **Technical Requirements**

To ensure an optimal experience, we recommend using a stable internet connection and an updated version of your preferred browser.

### **Contributing**

We are always open to improvements and new ideas. If you'd like to contribute to the development of EDfilms, feel free to submit pull requests or propose new features and absolutely don't ask question at the exam.
