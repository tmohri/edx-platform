define(['jquery', 'js/factories/login', 'common/js/spec_helpers/ajax_helpers', 'common/js/components/utils/view_utils'],
function($, LoginFactory, AjaxHelpers, ViewUtils) {
    'use strict';
    describe("Studio Login Page", function() {
        var submit_button;

        beforeEach(function() {
            loadFixtures('login.underscore');
            new LoginFactory("/home/");
            submit_button = $('#submit');
        });

        it('It will disable the submit button once it is clicked', function() {
            spyOn(ViewUtils, 'redirect').andCallFake(function(){});
            var requests = AjaxHelpers.requests(this);
            expect(submit_button).not.toHaveClass('is-disabled');
            submit_button.click();
            AjaxHelpers.respondWithJson(requests, {'success': true});
            expect(submit_button).toHaveClass('is-disabled');
        });

        it('It will not disable the submit button if there are errors in ajax request', function() {
            var requests = AjaxHelpers.requests(this);
            expect(submit_button).not.toHaveClass('is-disabled');
            submit_button.click();
            AjaxHelpers.respondWithError(requests, {});
            expect(submit_button).not.toHaveClass('is-disabled');
        });
    });
});
