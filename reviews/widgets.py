from django import forms


class MethodSelectWidget(forms.widgets.RadioSelect):
    template_name = 'partials/reviews/widgets/method_select_widget.html'
    option_template_name = 'partials/reviews/widgets/method_select_option.html'


class StarRatingWidget(forms.widgets.RadioSelect):
    template_name = 'partials/reviews/widgets/star_rating_widget.html'
    option_template_name = 'partials/reviews/widgets/star_rating_option.html'