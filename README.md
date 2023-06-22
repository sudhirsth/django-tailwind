# Django x Tailwindcss

Learn how to integrate Tailwind.css into your Django projects.

Tailwind is a paradigm shift for how you'll use CSS in your _all_ of your web applications and Django projects.  Instead of using classes like `btn-primary` you'll use a list of more robust classes to describe how you want your element to render. Such as:

- `bg-blue-500` (the background color)
- `text-white` (the text color)
- `rounded-lg` The border radius
- `hover:bg-blue-800` The background color when someone _hovers_ on this element
- `px-5` The horizontal padding on the left or the right of the contents

And so much more. Writing CSS classes like this is almost _too_ verbose since it seems to violate DRY but it does not. Instead, this verboseness unlocks a clarity in how you document your CSS classes and how things are rendered. 


__References__
- [Django Docs](https://djangoproject.com)
- [Tailwind.css Docs](https://tailwindcss.com)