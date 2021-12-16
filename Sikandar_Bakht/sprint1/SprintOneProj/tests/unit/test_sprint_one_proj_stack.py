import aws_cdk as core
import aws_cdk.assertions as assertions

from sprint_one_proj.sprint_one_proj_stack import SprintOneProjStack

# example tests. To run these tests, uncomment this file along with the example
# resource in sprint_one_proj/sprint_one_proj_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = SprintOneProjStack(app, "sprint-one-proj")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
