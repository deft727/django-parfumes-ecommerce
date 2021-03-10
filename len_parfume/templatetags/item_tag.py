from django import template
from len_parfume.models import Product,Whishlist,User
from django.utils.safestring import mark_safe



register = template.Library()




@register.simple_tag(takes_context=True)
def get_item(context,filter):
    request = context ['request']

    if not filter:
        return mark_safe("inactive")
    else:
        print(filter,'ecть',type(filter))
        product=Product.objects.get(id=filter)
        print(product)
        if request.user.is_authenticated:
            user = User.objects.filter(username=request.user).first()
            x=Whishlist.objects.filter(owner=user,products=product)
            print(x)
            if x:
                return mark_safe("active")
            else:
                return mark_safe("inactive")
        else:
            name = str(request.session.session_key)
            x=Whishlist.objects.filter(session=name,products=product)
            print(x)

            if x:
                return mark_safe("active")
            else:
                return mark_safe("inactive")



