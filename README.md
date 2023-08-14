# Secure Programming Assignment 2 

# Steps to run web app

1. Clone this repository into a folder on your computer.
2. Run "pip install virtualenv", if you don't have it already.
3. Run "virtualenv venv"
4. Run "source venv/bin/activate"
5. Run "pip install -r requirements.txt"
6. Run "python manage.py runserver" to start a localhost server for the app.
7. Open http://127.0.0.1:8000/ in browser to access web app
8. Run "deactivate" to quit the virtual environment.


# YouTube video explaining security implementations:

<https://www.youtube.com/watch?v=_G9X9Tvj_gw> 


# Credits:

1. Pranav Varun Chandran - a1879231

   1. Found the base code on which this project was built on
   2. Implemented Stripe payment functionality on the web app
   3. Added products to the catalog
   4. Maintained GitHub repository

2. Sampada Neupane - a1867737

   1. Implemented product review functionality

3. Sarfaraz Ahmed Basha - a1879900

   1. Identified Threats to be addressed on the web app
   2. Implemented Search Functionality vulnerable to DOM-based XSS
   3. Implemented custom users and user roles
   4. Implemented custom staff and admin dashboards and all its its functionalities
   5. Maintained GitHub repository


# Database Schema 
1. store_products
   1. id - primary key
   2. name - Product name
   3. price
   4. description
   5. image - Image location
   6. review - JSON with customer name and review
   7. category id - foriegn key
2. store_order
   1. id - primary key
   2. quantity
   3. price
   4. address
   5. phone
   6. date
   7. status - 0 or 1
3. store_category
   1. id - primary key
   2. name - Category name
4. store_customuser
   1. id - primary key
   2. password - sha256 hashed
   3. last_login
   4. is_superuser
   5. username
   6. first_name
   7. last_name
   8. email
   9. phone_number
   10. is_active
   11. is_staff
   12. is_admin
   13. user_id
5. store_role
   1. id - primary key
   2. name - Role name
   3. description
6. store_userrole
   1. id - primary key
   2. order_id
   3. role_id - foreign key
   4. user_id - foreign key

# Threats addressed by each member:

1. **Broken Access Control** by Pranav Varun Chandran - a1879231

2. **Cross Site Request Forgery (CSRF)** by Sampada Neupane - a1867737

3. **Cross-Site Scripting (XSS)**

   1. **Stored XSS** by Bivek Giri - a1866934
   2. **DOM-based XSS** by Sarfaraz Ahmed Basha - a1879900


# Broken Access Control

1. Three user roles have been defined:

![](https://lh5.googleusercontent.com/RQc68GKTj-WX6lP_I_jRKCssDy4nGBtbVOj3C-S8MvYvKDM_y7akD_ywbfZBjfCV3FSMO7QiGbKedhdQ64s2i6_ZvCD0K5odWV9L8pi3kS4DhQaQ6s1ZlmmH6opZ5hsQvBVvvid2IrAxtTLnirrczQ4)

2. Each role has specific permissions

![](https://lh5.googleusercontent.com/T37ZCOgHGNTpGG5LFJqAVSIVonZWSrITkl2eu99FqZFYLVm5hsyfT70oGbOAr-Wc2UOsPcZJm4u-v7ZQ2EshD9_nf8YWcTLB2pDHtfvxWP06KJJLo2Lwiu0u6cQj7GoSyZF_k2YyZ72tP2UkbSUC8Bo)

3. Both get and post requests check for admin roles using if conditions

![](https://lh3.googleusercontent.com/a7aWxeIX2sKgw_9FPC5Nc3Ea6AOUbkHL5nVanrOaqkxngjjxAe7jGJBMpO0dyhIXOr5w3-70Zp4B7VjCqFbjD0PWXJ7ptGWiUhwS-ViaQDJ9F9BoAKaYfJaF8Hzdj3e67owo9epJBt4A1r4NHd_FlfM)

4. The request.session.get will retrieve the customer id from the session token.


# Cross Site Request Forgery (CSRF)

CSRF (Cross Site Request Forgery) token plays a critical role in securing django ecommerce websites as it handles user’s data, payment information etc by ensuring that every form submission/POST request comes from trusted sites and not from potential attackers.

**CSRF (Cross Site Request Forgery)  prevention implementation**

Step 1: For this implementation let’s first try to login as a customer in the application. Before submitting the email and password the csrf token for the session is checked.

![](https://lh3.googleusercontent.com/tcphPNCQlZq98NYldR6ztB39Jzgg5WtuSU-QJdSSpRbDLBmeCGOmNfILIBYv23fJTArBWrrrHObzdQyjNrkTZu0EATuEa-9vHOIeu0tx5xnLLWU5FSrjH2Z5jKvniwd8YTXgIqyNgoI782uOdGX4lSs)

Step 2: Then the csrf token for the session is changed and login information is submitted. As the csrf token was changed and the session doesn’t recognise the token so a forbidden 403 error message is thrown out.

![](https://lh3.googleusercontent.com/J2yLehnPMFg3PqLARpDsQtWP2FVnCWqs7_vS1GLii49AHQxpftqrioBlICxsp775ygo9Lr3hKzACD3odHYvdpVg5S6UKIwH6nkpazQUwIuNvJirUPrMbafFb8kCfFovQ5luqqOKmA8mwSEt-Y8WHny4)

Step 3: The csrf token is changed back to its original token and again customer’s details are submitted to the site directly to the dashboard with the changed csrf token.

![](https://lh3.googleusercontent.com/84epF005o9yK-cTVEsCePagdm0pojk_DR6U0ehbEFrCrg_G79_BLRf9zUMe3vx4JFgdISR8_lSP0qauPEFaVeZeuUvaje7fd85zrF19U6FQiregBBNKNJCh9lmfspQwAnTJYmzhhres1EsQ0-1-YtkA)

**Code Implementation of CSRF in Code**

**Changes in _Eshop/settings.py_**

****![](https://lh3.googleusercontent.com/QzFb1_VY_ujrhdEKQe5SxlYTujoHv5igXaIzKfQvVO268Bwk4vVI2hU_81-O6X_j4vr_0FYeZCu-uk2hMZB063_j4k7ftIz-qFiHuRk-mHkB3QL57dPMQKIKNirh0dwCoWjzBB_cULI3RLE4ph1Dn9c)****

**Changes in _store/templates/login.html_**

****![](https://lh5.googleusercontent.com/gkEcm8v1whah2mnRThx-bNmlrnWG3EJZV8STMH5oCVfDHxPRu5_1Y6UsbNNT0I88Kxl53wS-6KzXHtJwW0s-8q27ispWUCOB5Tde3lBK4WdN1QVxyo9N-bozGLbIoLZv2_Y565UsfB71YGu0dTn4-dw)****

**Changes in _store/views/login.py_**

****![](https://lh6.googleusercontent.com/H1w20e4OlkG3udVJGW59BODi2-eTyq23kpioEE5DzgDW0D13Fj3IZ25eLsWwofjwu6zrTSSPtv2afxFh9mLraTP-1bGvFlRWh3Lo3qSqhUG7W8PaFH7yAJLSWZisnId8KqC7g4kwUZY9ToWpMrx5TOA)****


# Cross-Site Scripting (XSS)

## Stored XSS

Stored XSS:

This type of XSS permanently stored the malicious code injected from the user through input query fields like comment field, search field, forum and so on. Some malicious input that attacker can submit are like this:

\<script>/\* Malicious command…\*\</script>

Inorder to prevent our website from stored XSS, we can do following steps:

Step 1: Input Validation: Create a blacklist string that can be malicious and search that string in the input that user has submitted. We have used the ‘re’ library for searching strings. If any string matches the blacklist string, then it will display an “Invalid Input” message and ignore the input without storing it in the database. However, if it is not matched then it will move forward for data sanitization (in step 2).

![](https://lh4.googleusercontent.com/UBxGK49s_xtHYFVVFScf6pRxkCeCFyJ5ki7vMATjU8CXOv-0yC4CnWWBuVQTU6WQt1yuo7o_jNBKP0m5g0DSMyObKS-hvpYSXoiu2G-t-YJJbYv-ZcaAlFvXlzDTrv6V28oXbHWWRJ4aWqF2IiGxC4U)

Figure 1: Implementation of input validation in views

![](https://lh3.googleusercontent.com/ZKCDd_mf_6g19l1OFRKH5iKjx0zyudEJ8SxZQXcNHSU7b-YT6LymXY6EQGe37jPdv9GhB3L6coWNoqOGFVScCRIEOyzW_Y4QQYkBLPv41pO940z9Eh_hztM8VtiOWE84CA4RJf69Ou7PJZ2H9zLbUS0) 

Figure 2: Inputting malicious code![](https://lh3.googleusercontent.com/F3xcFW66Z4i2p3W8jqPEE0aOcDypNDFhNprH3pxzUWK6j-FRCLsK54f7_0cVfbqSDCaam8mhfhEOlJZ42FOkEApTKY0CvTKvWHBEcRB5TSHgqNsl1wNEoOV79pnEtvez8L2ZWPZSEWZLbF0WPQMixzk)

Figure 3: Message showing after inserting malicious code

 Step 2: Data Sanitization: We have used bleach library to sanitize the data. Sanitizing data is very important before inserting into the database. Attributes like ‘<’, ‘>’, ‘’’,’”’ into \&lt;\&gt is the process of sanitizing the data using bleach.

sani\_review= bleach.clean(review\_text)

 ![](https://lh3.googleusercontent.com/kDlRiq8u9v2f9miY47UjbUtx7-3BLxeSHFrCinHr-9adjwtL7jUFEGyq194GYIaj73ER3xmqETmwJ2C9D-s_nu2AuIfCN453WHoUxMa9FZrALcLOEdvbGfi3lKqjXxDGyvEt7XUv-PJimYVd2KF_XEE)

                          Figure 4: Inputting untrusted attributes

![](https://lh6.googleusercontent.com/-eUB842WJTtfFgRnwarntMxqbxgZcs1SOaG2ZGLEdkGlT_srgZYLhonBSpp1NZOODVOkCX_PyCXnVNV9NcL4ZgXkVgbOG6LFZe25HkBwXs6_fLLBmQrGmfVdnb8Cb_Pm0R7A8aesvSqWmB8JZG61fbU)

                          Figure 5: Sanitized data

 

Data stored in the database.

\[{"customer\_name": "bbb bbb", "review": "\&lt;hello\&gt;"}, {"customer\_name": "bbb bbb", "review": "\&lt;hello\&gt;"}]


## DOM-based XSS

Code vulnerable to DOM-based XSS in templates/search.html:

![](https://lh6.googleusercontent.com/Yjwxs9fYK_a8R0Fy8tSXH9MufvHp9Sjp1_2EpCdD0xax0jtUrrwb-MOdPiaUg6iB8mhxmYXeqjMJwcJIMABrF3zHz1EM79bM1NcE93SXFUxTiRv9Pb9tHEMP4dgStn8Peya1xLuz8e09pILxPCGcLk4)

The above code is vulnerable to DOM-based XSS as the response for a search request is just a list of all the products, and then using the above JavaScript code, the products are filtered. The part of the code that makes it vulnerable to DOM-based XSS is where the hashTerm is written to a document element with the ID of “results” using the .innerHTML method. 

Implementations to prevent DOM-based XSS:

1. Input Validation in templates/search.html:

![](https://lh6.googleusercontent.com/O4JX2dQrIgK4tZW2tVc8f07_HhMn3yCde4ly4j4dB5ezYeJNgzEVZvJr36SZPb3LaKRO2FDpQri-_TYoPxhb00OQgQkhrj8v-MV2cmuX94-g7Oxr61QnOg1GSv4mxYwK7H-yrwzVEzgrn62_1umXtZc)

The above code checks the searchTerm against a known-bad list of keywords and if the lowercase of the searchTerm matches to any one of the black-listed keywords, it returns False, else True.

2. Output Encoding

![](https://lh4.googleusercontent.com/_XQm6p_GzIppizJFkgiQXihkCBTTHjEnDmIktHg71Y0yfhCfD2BP2Bk6-iVo4LdTvtb5SWRN2T0izq8kVlLvdiObJbS13A0bHv9uY1Dfp96Z709IuS_t2oPH-eHcBZWbOdf24ViqLXt9qQnlVzOcCxc)

The above code replaces HTML entities in the searchTerm, which is unsafe, to its HTML entity encoding.

3. Content Security Policy

   1. Defining custom csp in middlewares/csp.py

![](https://lh4.googleusercontent.com/utVG5023dBdiRuTBgHZ7I2MaOnSbn3goJCpkbFtQfy0AZbcbdYvPYYq4dSHXZVhb3R4jg5UcaAbT2N1g19XG6NZiqkOR80oZid7wzzdF7oDE_MeLlJ8j_apSHLY6sntZtnwCDSk51RUZqremaq7xdE0)

The above code defines a custom CSP, where for script and style tags, inline tags with a random generated nonce is only executed by the web browser. Nonce was used, as this would provide a good security to in-line script and style tags, instead of going with unsafe-inline, which would have allowed for execution of any in-line script and style tags. Further, external script, style, frame, image, and font sources are specified. Additionally, an endpoint is provided for reporting of any and all csp-violations.

2. Logging CSP Violations in views/csp.py

![](https://lh3.googleusercontent.com/CnzFXV8WrRsqT_mrh25Ypm-m7_svjZDom2XUiJjN2_CeCSApFqGzE0L2I36pBh5qnzBKtqssHw3lVCRjSRiKFqycjDryr6656-DmqW9REyIhekBvlxIoT4E_sv7dHmDccX3MOFgCfCS9wpHApGWJPb0)

The above code logs in all requests that come to /csp-report to csp-reports.txt.

3. Nonce Value for Inline Style

![](https://lh4.googleusercontent.com/ohTE2x6apST24TxOsmGXRzabHBa10IQbHO1iC0KQY2yKhyO5DG33aM4uB3TlfauHR6Gqtu0_IEFqmg5bNHfxcQ6cNmJvL8QgJNvS-NNNkB9ZxYOfHqunUr9Uh4QewLxIYC5pE-jdrlNZ3dpar5BZwIA)

All in-line style tags are added with nonce="{{ request.nonce }}" so that it is not blocked by the CSP configuration.

![](https://lh4.googleusercontent.com/MetC7jOH8HuGF8wA07Ky2af0P8yAzdh_EY0cgbEPnScZbhrJiVXbSEjUzvDtEc6RNyBRtKi3Y17H-YoxaANbQtA8ZpMau7tJ2Z3JaYhVBSdc1LfDwIX5p2FTCqZ5xR78WtahyGSB6tYY4BDhLtItRao)

As the image tag had in-tag style which isn’t allowed by current CSP configuration, an inline-style was created to make the page be rendered the same without violating the CSP configuration.

4. Nonce Value for In-line Script tags

![](https://lh6.googleusercontent.com/eq-g8_1GC6PgYtFTDwvP9P0qO_YPdQLkgZLgStUIt_9jiHr8lkaCxNv559wNeca-ivAQytAjBFwqIgtaMR8OFTEJW09yntxL7h9T9t10BNY2N5AW0FBPmwpGvb1mOHA0BeOQ-m71siLAhrf0ALD51HI)

All in-line script tags are added with nonce="{{ request.nonce }}" so that it is not blocked by the CSP configuration.

5. Nonce Value for Search Submit button

![](https://lh3.googleusercontent.com/xK8tGipg5wX5AjFvMA2CwMLiQ9fvZ29ji7WZ63ms8zqt2CWkt3XzLllxlZ93OQntQwKmJ1ilHYrxB7p0uWGykfrvrB99loFmRTPek6EubO7gs_SuEXZoHxJ4dXDkUwH4gxbf0UBgi9rXYtpQjQiR2Fs)

There was a CSP violation when the Search submit button was requested. To not violate the CSP configuration set, a new script tag with the .addEventListener method was added to perform the same task.

Extra security implementation against XSS:

4. Cross-origin resource sharing (CORS)

![](https://lh5.googleusercontent.com/jHC8i9LsSUBhy893r4HQrZcNGLGTV-AVyyIpVTK7CNNTUaDh9R2xyP61YxphpVnWkVMusa5EnNQY-2w9TSbqVQodFZLot1DNCvgM1UzY50wIS9JOAOVfGX7vlCYoDo548Zciboj8lqLU2i9g6hfPriE)

CORS policy was added as an extra protection over CSP. CSP governs all the domains that this web app can request to, while CORS policy governs all the domains that can make requests to our domain. Thus, the above CORS configuration was added to be compatible with the CSP configuration.

