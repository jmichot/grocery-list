describe('grocery list', () => {
  before(() => {
    cy.visit('http://127.0.0.1:5000')
  })

  it('Add product', () => {
    cy.contains("Add Product").click()
    cy.contains("Product name *").find('input').type('Cypress Test')
    cy.contains("Product quantity *").find('input').type(5)
    cy.contains("Submit").click()
  })

  it('Found product in list', () => {
    cy.contains("Cypress Test").parent().find(".text-subtitle1").should(
      "have.text",
      "5"
    );
  })

  it('Add quantity', () => {
    cy.contains("Cypress Test").parent().parent().find('i:contains("add_circle")').click()
  })

  it('Test new quantity', () => {
    cy.contains("Cypress Test").parent().find(".text-subtitle1").should(
      "have.text",
      "6"
    );
  })

  it('Remove quantity', () => {
    cy.contains("Cypress Test").parent().parent().find('i:contains("remove_circle")').click()
  })

  it('Test new quantity', () => {
    cy.contains("Cypress Test").parent().find(".text-subtitle1").should(
      "have.text",
      "5"
    );
  })

  it('Modify product', () => {
    cy.contains("Cypress Test").parent().parent().find('i:contains("edit")').click()
    cy.contains("Product name *").find('input').type('Cypress Test Modif')
    cy.contains("Product quantity *").find('input').clear().type(10)
    cy.contains("Submit").click()
  })

  it('Test after modification', () => {
    cy.contains("Cypress Test Modif").parent().find(".text-subtitle1").should(
      "have.text",
      "10"
    );
  })



})