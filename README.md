# SLASH

Slash Your Spending, Not Your Style - Unleash the Best Deals!!

<p align="center"><img width="500" src="./assets/Shop.gif"></p>

[![GitHub license](https://img.shields.io/github/license/CSC510-SE-Fall2024/Team-82_Project-2)](https://github.com/CSC510-SE-Fall2024/Team-82_Project-2/blob/main/LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14018764.svg)](https://doi.org/10.5281/zenodo.14018764)
![Github](https://img.shields.io/badge/language-python-red.svg)
[![Discord](https://img.shields.io/discord/1300195209472114780?color=blueviolet&label=Discord%20Discussion%20Chat&cacheBuster=1)](https://discord.gg/UF5Hr2dW)
[![Run Tests On Push](https://github.com/CSC510-SE-Fall2024/Team-82_Project-2/actions/workflows/unit_test.yml/badge.svg)](https://github.com/CSC510-SE-Fall2024/Team-82_Project-2/actions/workflows/unit_test.yml)
[![codecov](https://codecov.io/gh/CSC510-SE-Fall2024/Team-82_Project-2/branch/main/graph/badge.svg?token=20a750d4-c013-4006-8a38-24bddf824450)](https://codecov.io/gh/CSC510-SE-Fall2024/Team-82_Project-2)
[![Lint Python](https://github.com/CSC510-SE-Fall2024/Team-82_Project-2/actions/workflows/pylint.yml/badge.svg)](https://github.com/CSC510-SE-Fall2024/Team-82_Project-2/actions/workflows/pylint.yml)
[![Close as a feature](https://github.com/CSC510-SE-Fall2024/Team-82_Project-2/actions/workflows/close_as_a_feature.yml/badge.svg)](https://github.com/CSC510-SE-Fall2024/Team-82_Project-2/actions/workflows/close_as_a_feature.yml)
[![Python Application](https://github.com/CSC510-SE-Fall2024/Team-82_Project-2/actions/workflows/python-package.yml/badge.svg)](https://github.com/CSC510-SE-Fall2024/Team-82_Project-2/actions/workflows/python-package.yml)
[![Python Style Checker](https://github.com/CSC510-SE-Fall2024/Team-82_Project-2/actions/workflows/style_checker.yml/badge.svg)](https://github.com/CSC510-SE-Fall2024/Team-82_Project-2/actions/workflows/style_checker.yml)
[![Running Code Coverage](https://github.com/CSC510-SE-Fall2024/Team-82_Project-2/actions/workflows/code_cov.yml/badge.svg)](https://github.com/CSC510-SE-Fall2024/Team-82_Project-2/actions/workflows/code_cov.yml)
[![GitHub issues](https://img.shields.io/github/issues/CSC510-SE-Fall2024/Team-82_Project-2)](https://github.com/CSC510-SE-Fall2024/Team-82_Project-2/issues)
[![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/CSC510-SE-Fall2024/Team-82_Project-2)](https://github.com/CSC510-SE-Fall2024/Team-82_Project-2/issues?q=is%3Aissue+is%3Aclosed)
[![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/CSC510-SE-Fall2024/Team-82_Project-2)](https://github.com/CSC510-SE-Fall2024/Team-82_Project-2/pulls?q=is%3Apr+is%3Aclosed)

<a href="https://github.com/CSC510-SE-Fall2024/Team-82_Project-2/network"><img alt="GitHub forks" src="https://img.shields.io/github/forks/CSC510-SE-Fall2024/Team-82_Project-2?cacheBuster=1"></a>
<a href="https://github.com/CSC510-SE-Fall2024/Team-82_Project-2/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/CSC510-SE-Fall2024/Team-82_Project-2?cacheBuster=1"></a>

Slash is a tool that scrapes the most popular e-commerce websites to get the best deals on searched items across these websites.
Currently supported websites include [Walmart](https://www.walmart.com/), [Target](https://www.target.com/), [BestBuy](https://www.bestbuy.com/), [Amazon](https://www.amazon.com/), [Google Shopping](https://shopping.google.com/), [Etsy](https://www.etsy.com/), and [EBay](https://www.ebay.com/).

- **Fast**: With slash, you can save over 50% of your time by comparing deals across websites within seconds
- **Easy**: Slash uses very easy commands to filter, sort and search your items
- **Powerful**: Quickly alter the commands to get desired results

# :rocket: Quick Guide

1. Access the Github repository from your computer.

- First, pre-install [git](https://git-scm.com/) on your machine.
- Then, clone the repo using the following command:

```
git clone https://github.com/CSC510-SE-Fall2024/Team-82_Project-2.git
```

- Finally, `cd` into the local repository.

```
cd slash
```

2. Run the installation script `install.py`:

- Execute the `install.py` script to handle all setup requirements automatically. This includes installing dependencies, setting up environment variables, and ensuring the project is ready to run.
- The script will prompt you for the following inputs: Google Client ID: Enter your OAuth 2.0 Client ID. Google Client Secret: Enter your OAuth 2.0 Client Secret. This input is handled securely.

```
python3 install.py
```

3. Run the project

- After installation, start the Flask application:

```
flask run
```

4. Access the application

- Open your web browser and navigate to:

```
http://localhost:5000
```

<p>
 
# :dizzy: What's New? (Project 2 Updates)

### Added Google OAuth login feature

## 🔑 **Setting up Google OAuth Login**

Follow these steps to configure and enable Google OAuth login:

### 1️⃣ **Create a Google OAuth App**

1. Visit the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Enable the necessary APIs:

   - Go to **APIs & Services > Library**.
   - Search for **Google Identity API** and enable it.

4. **Set up the OAuth Consent Screen**:

   - Navigate to **APIs & Services > OAuth consent screen**.
   - Choose **External** as the User Type.
   - Provide essential details like **App Name**, **Support Email**, and **Developer Contact Info**.
   - Add OAuth scopes:
     - `email`
     - `profile`
     - `openid`
   - Save and **Publish** the consent screen.

5. **Create OAuth Credentials**:
   - Go to **APIs & Services > Credentials**.
   - Click **Create Credentials > OAuth Client ID**.
   - Choose **Web Application** as the Application Type.
   - Add an **Authorized Redirect URI**:  
     `http://localhost:5000/google/callback`
   - Save the **Client ID** and **Client Secret** for use in your application.

---

### 2️⃣ **Configure OAuth in Your Code**

1. Add your **Google Client ID** and **Client Secret** to the config file:
   ```python
    client_id='', # Place your OAuth Client ID here
    client_secret='', # Place your OAuth Client secret here
   ```

### Other Enhancements:

- **More websites added for scrapping -Ebay, Target, Bestbuy**
- User Wishlist dynamically updates the price.
- New workflows added to the repository.
- Extended test coverage of the repository.

## :movie_camera: Checkout our demo video

[![Video](https://img.youtube.com/vi/5iCc2LJa_bI/0.jpg)](https://youtu.be/5iCc2LJa_bI)

# :muscle: What's next for future development?

- Streamlined Customer Experience: Implement a seamless ordering and payment system directly on the website, allowing customers to effortlessly place orders with just a few clicks, thereby enhancing user satisfaction and convenience.
- Enhanced Security Features: Strengthen the login module by integrating tokenization, adding an extra layer of security to user accounts. This advanced security measure ensures a secure and reliable user authentication process.
- Database Integration: Add database to open gateway further enhancements to the project.
- Advanced Inventory Insights: Provide parameters like in-store availability.
- Additional Account Settings: Introduce additional account settings to give users more control over their profiles and preferences, enhancing their personalization and usability.
- Predictive Model: Develop a predictive model that can determine the optimal timing for purchasing the least expensive product from the search results. This feature will provide valuable guidance to users, helping them make informed decisions.
- Enhanced Search Capabilities: Improve the search functionality by introducing advanced search capabilities. This can include options for filtering search results based on ratings, price ranges, and other relevant criteria, giving users more refined search options.
- Multi-Platform Integration: Expand the platform's capabilities by incorporating search results from various e-commerce platforms such as Dick's Sporting Goods, and more. This will provide users with optimized outcomes from a diverse selection of online vendors.
- Social Media Login: Add support for different methods of login, such as Gmail, Facebook, or other social media accounts, to provide users with convenient and secure login options.
- Price Chart Visualization: Introduce a visual representation of price trends for products. This feature can help users understand historical price changes and make more informed purchasing decisions.
- UI Enhancement: Continue to enhance the user interface to provide an even better user experience. Consider improving aesthetics, user-friendliness, and overall design.
- Containerization: Implement Dockerization of the project to enhance its scalability, portability, and overall deployment efficiency.

## :thought_balloon: Use Case

- **_Students_**: Students coming to university are generally on a budget and time constraint and generally spend hours wasting time to search for products on Websites. Slash is the perfect tool for these students that slashes all the unnecessary details on a website and helps them get prices for a product across multiple websites.Make the most of this tool in the upcoming Black Friday Sale.
- **_Data Analysts_**: Finding data for any project is one of the most tedious job for a data analyst, and the datasets found might not be the most recent one. Using slash, they can create their own dataset in real time and format it as per their needs so that they can focus on what is actually inportant.


## Score Card
---
#### Total Grade: 145

| Factor | Score | Notes |
| --- | --- | --- |
| Video | 3 | Link Updated (https://www.youtube.com/watch?v=Fp7tj_xCvBc) |
| Workload | 3 | Distributed |
| Number of commits | 3 | 50+ |
| Number of commits: by different people | 3 | https://github.com/CSC510-SE-Fall2024/Team-82_Project-2/graphs/contributors?from=28%2F09%2F2024 |
| Issues report: There are many | 2 | https://github.com/CSC510-SE-Fall2024/Team-82_Project-2/pulse |
| Issues are being closed | 2 | https://github.com/CSC510-SE-Fall2024/Team-82_Project-2/pulse |
| DOI badge | 3 |  |
| Docs: format | 3 |  |
| Docs: description  | 3 |  |
| Docs: short animated video | 2 |  |
| Docs: strong punchlines | 3 |  |
| Docs: mini tutorials | 3 |  |
| Use of version control tools | 2 |  |
| Use of style checkers | 3 |  |
| Use of code formatters. | 3 |  |
| Use of syntax checkers. | 3 |  |
| Use of code coverage | 3 |  |
| Other automated analysis tools | 2 |  |
| Test cases exist | 3 |  |
| Test cases are routinely executed | 2 |  |
| The files http://contributing.md/ lists coding standards and lots of tips | 3 |  |
| Issues are discussed before they are closed | 3 |  |
| Chat channel: exists | 3 |  |
| Test cases: a large proportion of the issues related to handling failing cases. | 2 |  |
| Evidence that the whole team is using the same tools | 3 |  |
| Evidence that the members of the team are working across multiple places in the code base | 2 |  |
| Short release cycles | 3 |  |
| Does your website and documentation provide a clear, high-level overview of your software? | 3 |  |
| Does your website and documentation clearly describe the type of user who should use your software? | 3 |  |
| Do you publish case studies to show how your software has been used by yourself and others? | 3 |  |
| Is the name of your project/software unique? | 3 |  |
| Is your project/software name free from trademark violations? | 2 |  |
| Is your software available as a package that can be deployed without building it? | 3 |  |
| Is your software available for free? | 3 |  |
| Is your source code publicly available to download, either as a downloadable bundle or via access to a source code repository? | 3 |  |
| Is your software hosted in an established, third-party repository like GitHub? | 3 |  |
| Is your documentation clearly available on your website or within your software? | 3 |  |
| Does your documentation include a "quick start" guide, that provides a short overview of how to use your software with some basic examples of use? | 2 |  |
| If you provide more extensive documentation, does this provide clear, step-by-step instructions on how to deploy and use your software? | 3 |  |
| Do you provide a comprehensive guide to all your software’s commands, functions and options? | 3 |  |
| Do you provide troubleshooting information that describes the symptoms and step-by-step solutions for problems and error messages? | 3 |  |
| If your software can be used as a library, package or service by other software, do you provide comprehensive API documentation? | 3 |  |
| Do you store your documentation under revision control with your source code? | 2 |  |
| Do you publish your release history e.g. release data, version numbers, key features of each release etc. on your web site or in your documentation? | 3 |  |
| Does your software describe how a user can get help with using your software? | 3 |  |
| Does your website and documentation describe what support, if any, you provide to users and developers? | 3 |  |
| Does your project have an e-mail address or forum that is solely for supporting users? | 3 |  |
| Are e-mails to your support e-mail address received by more than one person? | 3 |  |
| Does your project have a ticketing system to manage bug reports and feature requests? | 2 |  |
| Is your project's ticketing system publicly visible to your users, so they can view bug reports and feature requests? | 3 |  |

# Additional Information

For Additional Information direct to this [page](https://github.com/SE23-Team44/slash/tree/main/docs) and check all the markdown files

# Chat Channel

<code><a href="https://discord.gg/KFtvmngMMD" target="_blank"><img height="100" width="250" src="https://user-images.githubusercontent.com/42767118/135394825-26dee6db-7a64-4e3f-902a-1e35abd4cf0c.png"></a></code>

## :sparkles: Contributors

<table>
  <tr>
    <td align="center"><a href="https://github.com/girish1430"><img src="https://avatars.githubusercontent.com/u/57136088?v=4" width="75px;" alt=""/><br /><sub><b>Girish G N</b></sub></a></td>
    <td align="center"><a href="https://github.com/joeljogy"><img src="https://avatars.githubusercontent.com/u/28514673?v=4" width="75px;" alt=""/><br /><sub><b>Joel Jogy George</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/prav29"><img src="https://avatars.githubusercontent.com/u/38226613?v=4" width="75px;" alt=""/><br /><sub><b>Pravallika Vasireddy</b></sub></a><br /></td>
  </tr>
</table>

## :email: Support

For support and inquiries related to **WolfTrack 6.0**, please contact us at **csc510group77@gmail.com**. We are here to assist you and address any questions or issues you may have.

We appreciate your interest and look forward to providing you with the best possible support and updates.
