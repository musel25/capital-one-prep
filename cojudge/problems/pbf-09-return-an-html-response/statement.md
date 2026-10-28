You use FastAPI primarily to build APIs, but it can also be used as a web framework (although we think Django is a better option for this).
You can install Jinja2 and return a template response as shown here.
However on our platform we work with single test and exercise files so in this Bite you will return an HTMLResponse with embedded HTML (docs). The effect will be the same though: the food log of a user in a nice html table!

| Food | Added | Servings | Calories (kcal) |
| --- | --- | --- | --- |
| egg | 2022-03-13 11:02:37.500968 | 1.5 x piece | 117.0 |
| oatmeal | 2022-03-13 11:02:37.500968 | 2.0 x 100 grams | 672.0 |

We provided the show_foods_for_user endpoint stub, add the logic to build up the HTML for the response. For your convenience we already added some template constants you can use: HTML_TEMPLATE and TABLE_ROW.
Here is what the final HTML response would look like as per the tests:

```html
<html lang="en"><head>  <meta charset="utf-8">  <meta name="viewport" content="width=device-width, initial-scale=1">  <title>Food log for Julian</title></head><body>    <table>        <thead>            <th>Food</th>            <th>Added</th>            <th>Servings</th>            <th>Calories (kcal)</th>        </thead>        <tbody>              <tr>                  <td>egg</td>                  <td>2022-03-13 11:02:37.500968</td>                  <td>1.5 x piece</td>                  <td>117.0</td>              </tr>              <tr>                  <td>oatmeal</td>                  <td>2022-03-13 11:02:37.500968</td>                  <td>2.0 x 100 grams</td>                  <td>672.0</td>              </tr>        </tbody>    </table></body></html>
```

Good luck and in the next and final FastAPI Bite we will add authentication to the API.

**Constraints:**

- Use GET `/{username}`. Preserve insertion order. Escape text fields in HTML. An unknown username gets an empty table.
