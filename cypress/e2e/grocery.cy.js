describe('grocery list', () => {
  before(() => {
    cy.visit('http://127.0.0.1:5000')
  })

  it('Add product', () => {
    cy.contains("Add Product").click()
    cy.contains("Product name *").find('input').clear().type('Cypress Test')
    cy.contains("Product quantity *").find('input').clear().type(5)
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
    cy.contains("Product name *").find('input').clear().type('Cypress Test Modif')
    cy.contains("Product quantity *").find('input').clear().type(10)
    cy.contains("Submit").click()
  })

  it('Test after modification', () => {
    cy.contains("Cypress Test Modif").parent().find(".text-subtitle1").should(
      "have.text",
      "10"
    );
  })

  it('Search product', () => {
    cy.contains("Search").parent().find('input').clear().type('T')
    cy.contains("Cypress Test Modif").parent().find(".text-subtitle1").should(
      "have.text",
      "10"
    )
    cy.contains("Search").parent().find('input').clear().type('TM')
    cy.get('.q-page').find(".q-list").should('have.length', 0)
  })

  it('Delete Product', () => {
    cy.contains("Search").parent().find('input').clear()
    cy.contains("Cypress Test").parent().parent().find('i:contains("delete")').click()
    cy.get('.q-page').find(".q-list").should('have.length', 0)
  })
  
  it('Menu', () => {
    cy.get(".q-layout--prevent-focus").should('have.length', 0)
    cy.contains("menu").click()
  })

  it ('Hide Drawer', () => {
    cy.get(".q-layout--prevent-focus").should('have.length', 1)
  })

  it ('Store click', () => {
    cy.contains("menu").click()
    cy.contains('store').parent().parent().click()
  })




})