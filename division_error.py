# defining an function to occur divided by 0 error
def division_zero(number1,number2):
    # using an try block, if number 2 is 0, there occur an divided by 0 
    try:
        result =number1/number2
        print("Result:", result)
        
    except ZeroDivisionError as e:
        print("Error:", e)

# we are calling the function
division_zero(10, 2) # No error, result will be print
division_zero(10, 0)# The Diviision by zero error will occur

# Now, We need to Introduce an intentional error to prevent the script from running successfully
some_variable = non_existent_variable