###For Collaborators of repo and Members of the Community
* Prefer making a separate branch for your work. It is fine if you directly make changes in master branch but then be extra careful since now our website is directly hosted through Github.
<br>

###General
* Add any additional files in appropriate folders. Make folder if necessary with meaningful names.
* Keep the code properly indented and add precise comments for others to understand
* Since we have used plain CSS for the webpage (not SCSS or frameworks), keep adding the section class name in CSS declarations even if it works without it. For example, CSS should be `.home h1 {font-size: 20vw;}` instead of `h1 {font-size: 20vw;}` where 'home' is class name of the section
* Every Section in HTML should have the same unique name and ID (used for CSS)
* Don't mix CSS and Javascript codes in HTML files. Keep them in designated files in the 'static' folder
* All script files are declared at the end of HTML to reduce the loading time of the page